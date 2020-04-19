from flask import render_template, flash, redirect, url_for, request, send_file
from flask import current_app, jsonify
from app import mongo, bcrypt
import gridfs
from .forms import (LoginForm, NewTypeForm, SearchedItemForm, SearchedItemListForm, StoreForm,
    SearchInventoryForm, NewSubTypeForm, MirrorForm, LocationsForm, formDict)
from .models import InStock, User
from bson import ObjectId
import json
from .select_lists import choices, get_search_fields
from .func_helpers import (get_products_and_stocks, get_productDict, update_productDict,
                           get_roomList, get_storageList, save_room, save_storage, delete_room,
                           delete_storage, set_query)
from flask_login import login_user, current_user, logout_user, login_required

fs = gridfs.GridFS(mongo.db)


@current_app.route('/', methods = ['GET', 'POST'])
@current_app.route('/index', methods = ['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user_db = mongo.db.user.find_one({'username':username})
        if user_db and bcrypt.check_password_hash(user_db['password'], password):
            user = User(id=user_db['_id'], username=user_db['username'], password=user_db['password'])
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful', 'success')

            return redirect(next_page) if next_page else redirect(url_for('main'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form)


@current_app.route('/main')
@login_required
def main():
    return render_template('main.html')


@current_app.route("/logout")
def logout():
    logout_user()
    flash('You are logged out', 'info')
    return redirect(url_for('index'))


@current_app.route('/item/new', methods = ['GET', 'POST'])
@login_required
def newItem():
    form = SearchInventoryForm()

    if form.is_submitted():
        group = form.searchType.data
        subgroup = form.searchSubtype.data.upper()
        return redirect(url_for('newItemEntry', group=group, subgroup=subgroup))
    
    return render_template('newItem.html', form=form, choices=choices)


@current_app.route('/item/new/<group>/<subgroup>', methods = ['GET', 'POST'])
@login_required
def newItemEntry(group, subgroup):
    form = formDict[subgroup]()

    if form.is_submitted():
        newProduct = get_productDict(subgroup, form.data)
        checkNewProduct = mongo.db.products.find_one({'_id':newProduct['_id']})
        if checkNewProduct:
            flash('Item already in the database.', 'info')
        else:
            docs = request.files.getlist(form.documentation.name)
            if docs[0].filename!='':
                newProduct['documentation'] = dict()
                for doc in docs:
                    uid = fs.put(doc, filename=doc.filename)
                    newProduct['documentation'][str(uid)]=doc.filename

            mongo.db.products.insert_one(newProduct)
            flash(f'Item added: {newProduct["_id"]}', 'success')
        
            return redirect(url_for('viewItem', itemId=newProduct['_id']))

    return render_template('newItemEntry.html', group=group, subgroup=subgroup, form=form, html_form=f'forms/{subgroup}.html')    


@current_app.route('/item/update/<itemId>', methods= ['GET', 'POST'])
@login_required
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
        if docs[0].filename!='':
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

    return render_template('updateItem.html', title=f'Update {itemId}',
                           form=form, itemId=itemId, itemDoc=itemDoc, html_form=f'forms/{item["type"]}.html')


@current_app.route('/item/delete/<itemId>', methods= ['GET', 'POST'])
@login_required
def deleteItem(itemId):
    mongo.db.products.delete_one({'_id':itemId})
    flash(f'Item {itemId} removed from database.', 'info')
    return redirect(url_for('main'))


@current_app.route('/inventory/search', methods = ['GET', 'POST'])
@login_required
def searchInventory():
    form = SearchInventoryForm()
    if form.is_submitted():
        subtype = form.searchSubtype.data.upper()
        searchFields = [form.searchField1.data, form.searchField2.data, form.searchField3.data]
        searchValues = [form.searchValue1.data, form.searchValue2.data, form.searchValue3.data]
        query = set_query(subtype, searchFields, searchValues)

        return redirect(url_for('inventory', query=query))

    return render_template('searchInventory.html', title='Search inventory',
                           form=form, choices=choices)


@current_app.route('/inventory/<query>', methods = ['GET', 'POST'])
@login_required
def inventory(query):
    form = SearchedItemListForm()
    print('query', query, flush=True)
    json_query = json.loads(query.replace("'", "\""))
    products, stocks = get_products_and_stocks(json_query)

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
                local_query = { '_id': litem['_id'] }
                if quantity == 0:
                    mongo.db.instock.delete_one(local_query)
                    flash(f'Item removed.', 'info')
                if litem['quantity']  != quantity:
                    newvalues = { '$set': { 'quantity': quantity } }
                    mongo.db.instock.update_one(local_query, newvalues)
                    flash(f'Item quantity changed.', 'success')
            else:
                flash(f'Quantity should be an integer.', 'danger')
        
        return redirect(url_for('inventory', query=query))
    
    return render_template('inventory.html', title='Inventory', form=form, products=products, query=query)


@current_app.route('/item/view/<itemId>', methods = ['GET', 'POST'])
@login_required
def viewItem(itemId):
    product = mongo.db.products.find_one({'_id':itemId})
    id = product.pop('_id')
    return render_template('viewItem.html', title=id, product=product, id=id)


@current_app.route('/item/store/<itemId>', methods=['GET', 'POST'])
@login_required
def storeItem(itemId):
    form = StoreForm()
    form.roomSelect.choices = get_roomList()
    form.storageSelect.choices = [('','')]

    if form.is_submitted() and form.roomSubmit.data:
        form.storageSelect.choices = get_storageList(form.roomSelect.data)

    if form.is_submitted() and form.submit.data:
        newStock = InStock(code=itemId,
                           quantity=int(form.quantity.data), 
                           room=form.roomSelect.data,
                           storage=form.storageSelect.data)
        query = {'$and':[{'code':newStock.code},
                         {'room':newStock.room},
                         {'storage':newStock.storage}]}

        oldStock = mongo.db.instock.find_one_and_update(query,
                                               {'$inc': {'quantity': newStock.quantity},
                                                '$set': {'stocked_date':newStock.stocked_date}})
        if oldStock == None:
            mongo.db.instock.insert_one(vars(newStock))
        flash(f'{newStock.quantity} {newStock.code} stocked in {newStock.room}, {newStock.storage}', 'info')

    return render_template('storeItem.html', title='Store item', form=form, itemId=itemId)


@current_app.route("/uploads/<string:id>")
@login_required
def get_upload(id):
    fin = fs.find_one({'_id':ObjectId(id)})
    data = fin.read()
    fext = fin.filename[-4:]
    tmpfile = current_app.config['TMP']+'tmpfile'+fext
    with open(tmpfile, 'wb') as fout:
        fout.write(data)
    
    return send_file(tmpfile)


@current_app.route('/delete/<string:itemId>/<string:docId>')
@login_required
def delete_document(itemId, docId):
    fs.delete(ObjectId(docId))
    product = mongo.db.products.find_one({'_id':itemId})
    product['documentation'].pop(docId)
    if len(product['documentation'])>0:
        mongo.db.products.update_one({'_id':itemId}, {'$set':{'documentation':product['documentation']}})
    else:
        mongo.db.products.update_one({'_id':itemId}, {'$unset':{'documentation':1}})
    
    return redirect(url_for('updateItem', itemId=itemId))
 

@current_app.route('/locations', methods=['GET', 'POST'])
@login_required
def locations():
    try:
        form = LocationsForm(roomList=request.args.get('roomDefault'))
    except NameError:
        form = LocationsForm()
    form.roomList.choices = get_roomList()
    try:
        form.storageList.choices = get_storageList(request.args.get('roomDefault'))
    except KeyError:
        form.storageList.choices = [('','')]
    
    if form.validate_on_submit() and form.addRoom.data:
        if form.room.data !='':
            newRoom = save_room(form.room.data)
            roomDefault = newRoom
            flash(f'Room {newRoom} added.')
        else:
            flash('Provide a proper room name as string.', 'danger')

        return redirect(url_for('locations', roomDefault=roomDefault))
    
    if form.validate_on_submit() and form.addStorage.data:
        if form.storage.data !='':
            print(form.roomList.data, form.storage.data)
            newStorage = save_storage(form.roomList.data, form.storage.data)
            flash(f'storage {newStorage} added in room {form.roomList.data}.', 'info')
        else:
            flash('Provide a proper storage name as string.', 'danger')
        
        return redirect(url_for('locations', roomDefault=form.roomList.data))

    if form.validate_on_submit() and form.viewStorage.data:
        return redirect(url_for('locations', roomDefault=form.roomList.data))

    if form.validate_on_submit() and form.delete_room.data:
        delete_room(form.roomList.data)
        flash(f'Room {form.roomList.data} has been deleted.', 'info')
        
        return redirect(url_for('locations'))

    if form.validate_on_submit() and form.delete_storage.data:
        delete_storage(form.roomList.data, form.storageList.data)
        flash(f'Storage {form.storageList.data} has been deleted.', 'info')
        return redirect(url_for('locations', roomDefault=form.roomList.data))
    
    return render_template('locations.html', title='Locations', form=form)


@current_app.route('/get_searchfield', methods=['GET', 'POST'])
@login_required
def get_searchfield():
    selection = request.args.get('selection').lower()
    try:
        dict_fields = dict(get_search_fields['base'], **get_search_fields[selection])
    except KeyError:
        dict_fields = get_search_fields['base']

    return jsonify(result=dict_fields)