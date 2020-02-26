from flask import render_template, flash, redirect, url_for, request, send_file
from flask import current_app
from app import mongo
import gridfs
from .forms import (NewTypeForm, SearchedItemForm, SearchedItemListForm, StoreForm,
    SearchInventoryForm, NewSubTypeForm, MirrorForm, LocationsForm, formDict)
from .models import InStock
from bson import ObjectId
import json
from .select_lists import optics_choices
from .func_helpers import (get_products_and_stocks, get_productDict, update_productDict,
                           set_roomList, set_storageList, save_room, save_storage, delete_room,
                           delete_storage)

fs = gridfs.GridFS(mongo.db)

@current_app.route('/')
@current_app.route('/index')
def index():
    return render_template('base.html')


@current_app.route('/item/new', methods = ['GET', 'POST'])
def newItem():
    typeform = NewTypeForm()

    if typeform.validate_on_submit():
        return redirect(url_for('newItemGroup', group=typeform.group.data))
    
    return render_template('newItem.html', title='Add item', typeform=typeform)


@current_app.route('/item/new/<group>', methods = ['GET', 'POST'])
def newItemGroup(group):
    subtypeform = NewSubTypeForm()
    if group=='optics':
        subtypeform.subgroup.choices = optics_choices

    if subtypeform.validate_on_submit():
        subgroup = subtypeform.subgroup.data
        return redirect(url_for('newItemEntry', group=group, subgroup=subgroup))    

    return render_template('newItemGroup.html', title='Add item', group=group, subtypeform=subtypeform)   


@current_app.route('/item/new/<group>/<subgroup>', methods = ['GET', 'POST'])
def newItemEntry(group, subgroup):
    form = formDict[subgroup]()

    if form.is_submitted():
        newProduct = get_productDict(subgroup, form.data)
        checkNewProduct = mongo.db.products.find_one({'_id':newProduct['_id']})
        if checkNewProduct:
            flash('Item already in the database.')
        else:
            docs = request.files.getlist(form.documentation.name)
            if docs:
                newProduct['documentation'] = dict()
                for doc in docs:
                    uid = fs.put(doc, filename=doc.filename)
                    newProduct['documentation'][str(uid)]=doc.filename

            mongo.db.products.insert_one(newProduct)
            flash(f'Item added: {newProduct["_id"]}')
        
            return redirect(url_for('viewItem', itemId=newProduct['_id']))

    return render_template('newItemEntry.html', title='Add item', group=group, subgroup=subgroup, form=form)    


@current_app.route('/item/update/<itemId>', methods= ['GET', 'POST'])
def updateItem(itemId):
    item = mongo.db.products.find_one({'_id':itemId})
    if 'documentation' in item.keys():
        itemDoc = item.pop('documentation')
    else:
        itemDoc = None 
    form = formDict[item['type']](data=item)

    if form.is_submitted() and request.method=='POST':
        updateDict = update_productDict(itemId, form.data)
        docs = request.files.getlist(form.documentation.name)
        if docs and docs[0].filename!='':
            print('there are docs')
            if 'documentation' not in item.keys():
                updateDict['documentation'] = dict()
            else:
                updateDict['documentation'] = item['documentation']
            for doc in docs:
                uid = fs.put(doc, filename=doc.filename)
                updateDict['documentation'][str(uid)]=doc.filename
        if len(updateDict)>0:
            mongo.db.products.update_one({'_id':itemId},
                                         {'$set':updateDict}, upsert=True)
        return redirect(url_for('viewItem', itemId=itemId))

    return render_template('updateItem.html', title='Update item',
                           form=form, itemId=itemId, itemDoc=itemDoc)


@current_app.route('/inventory/search', methods = ['GET', 'POST'])
def searchInventory():
    form = SearchInventoryForm()
    if form.validate_on_submit():
        if form.searchField.data=='part_number':
            value = (form.searchValue.data).upper()
            query = f'{{ "{form.searchField.data}":{{"$regex":".*{value}.*"}} }}'
            print(query)
        elif form.searchField.data=='room':
            value = (form.searchValue.data).upper().replace(' ', '')
            query = {form.searchField.data:value}
        else:
            value = (form.searchValue.data).upper()
            query = {form.searchField.data:value}

        return redirect(url_for('inventory', query=query))

    return render_template('searchInventory.html', title='Search inventory',
                           form=form)


@current_app.route('/inventory', methods = ['GET', 'POST'])
def inventory():
    form = SearchedItemListForm()
    query = json.loads(request.args.get('query').replace("'", "\""))
    products, stocks = get_products_and_stocks(query)

    if request.method == 'GET':
        for stock in stocks:
            item = dict(zip(('id_', 'code', 'room', 'storage',
                             'stocked_date', 'quantity'), 
                            (stock['_id'],stock['code'],stock['room'],
                             stock['storage'],stock['stocked_date'].strftime('%Y-%m-%d'),
                             stock['quantity'])
                            )
                        )
            form.items.append_entry(item)

    if form.is_submitted():
        for litem, fitem in zip(stocks, form.items):
            quantity = fitem.quantity.data
            if isinstance(quantity, int) and quantity >= 0:
                query = { '_id': litem['_id'] }
                if quantity == 0:
                    mongo.db.instock.delete_one(query)
                    flash(f'Item removed: {litem["_id"]} {fitem.id_.data}.')
                if litem['quantity']  != quantity:
                    newvalues = { '$set': { 'quantity': quantity } }
                    mongo.db.instock.update_one(query, newvalues)
                    flash(f'Item changed: {litem["_id"]} {quantity}.')
            else:
                flash(f'Quantity for item {litem["_id"]} should be an integer.')
        
        return redirect(url_for('inventory', query=query))
    
    return render_template('inventory.html', title='Inventory', form=form, products=products)


@current_app.route('/item/view/<itemId>', methods = ['GET', 'POST'])
def viewItem(itemId):
    product = mongo.db.products.find_one({'_id':itemId})
    id = product.pop('_id')
    return render_template('viewItem.html', title='Item', product=product, id=id)


@current_app.route('/item/store/<itemId>', methods=['GET', 'POST'])
def storeItem(itemId):
    form = StoreForm()
    form.roomSelect.choices = set_roomList()
    form.storageSelect.choices = [('','')]

    if form.is_submitted() and form.roomSubmit.data:
        form.storageSelect.choices = set_storageList(form.roomSelect.data)

    if form.is_submitted() and form.submit.data:
        newStock = InStock(code=itemId,
                           quantity=int(form.quantity.data), 
                           room=form.roomSelect.data,
                           storage=form.storageSelect.data)
        mongo.db.instock.insert_one(vars(newStock))
        flash(f'{newStock.quantity} {newStock.code} stocked in {newStock.room}, {newStock.storage}')
        

    return render_template('storeItem.html', title='Store item', form=form, itemId=itemId)


@current_app.route("/uploads/<string:id>")
def get_upload(id):
    fin = fs.find_one({'_id':ObjectId(id)})
    data = fin.read()
    fext = fin.filename[-4:]
    tmpfile = current_app.config['TMP']+'tmpfile'+fext
    with open(tmpfile, 'wb') as fout:
        fout.write(data)
    
    return send_file(tmpfile)


@current_app.route('/delete/<string:itemId>/<string:docId>')
def delete_document(itemId, docId):
    fs.delete(ObjectId(docId))
    product = mongo.db.products.find_one({'_id':itemId})
    product['documentation'].pop(docId)
    if len(product['documentation'])>0:
        mongo.db.products.update_one({'_id':itemId}, {'$set':{'documentation':product['documentation']}})
    else:
        mongo.db.products.update_one({'_id':itemId}, {'$unset':{'documentation':1}})
    
    return redirect(url_for('updateItem', itemId=itemId))
 

@current_app.route('/locations/', methods=['GET', 'POST'])
def locations():
    try:
        form = LocationsForm(roomList=request.args.get('roomDefault'))
    except NameError:
        form = LocationsForm()
    form.roomList.choices = set_roomList()
    try:
        form.storageList.choices = set_storageList(request.args.get('roomDefault'))
    except KeyError:
        form.storageList.choices = [('','')]
    
    if form.validate_on_submit() and form.addRoom.data:
        if form.room.data !='':
            newRoom = save_room(form.room.data)
            roomDefault = newRoom
            flash(f'Room {newRoom} added.')
        else:
            flash('Provide a proper room name as string.')

        return redirect(url_for('locations', roomDefault=roomDefault))
    
    if form.validate_on_submit() and form.addStorage.data:
        if form.storage.data !='':
            print(form.roomList.data, form.storage.data)
            newStorage = save_storage(form.roomList.data, form.storage.data)
            flash(f'storage {newStorage} added in room {form.roomList.data}.')
        else:
            flash('Provide a proper storage name as string.')
        
        return redirect(url_for('locations', roomDefault=form.roomList.data))

    if form.validate_on_submit() and form.viewStorage.data:
        return redirect(url_for('locations', roomDefault=form.roomList.data))

    if form.validate_on_submit() and form.delete_room.data:
        delete_room(form.roomList.data)
        flash(f'Room {form.roomList.data} has been deleted')
        
        return redirect(url_for('locations'))

    if form.validate_on_submit() and form.delete_storage.data:
        delete_storage(form.roomList.data, form.storageList.data)
    
        return redirect(url_for('locations', roomDefault=form.roomList.data))
    
    return render_template('locations.html', title='Locations', form=form)