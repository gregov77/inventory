from flask import render_template, flash, redirect, url_for, request, send_file
from flask import current_app
from app import mongo
import gridfs
from .forms import (NewTypeForm, SearchedItemForm, SearchedItemListForm,
    SearchInventoryForm, NewSubTypeForm, MirrorForm, formDict)
from .models import Product, InStock
from bson import ObjectId
import json
from .select_lists import optics_choices
from .func_helpers import listOfSearchedItems, createProductDict

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
        newProduct = createProductDict(subgroup, form.data)
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
                # for doc, doc_name in zip(docs, newProduct['documentation']):
                #     mongo.save_file(doc_name, doc)
            mongo.db.products.insert_one(newProduct)
            flash(f'Item added: {newProduct["_id"]}')
        
            return redirect(url_for('viewItem', itemId=newProduct['_id']))

    return render_template('newItemEntry.html', title='Add item', group=group, subgroup=subgroup, form=form)    


@current_app.route('/item/update/<itemId>', methods= ['GET', 'POST'])
def updateItem(itemId):
   item = mongo.db.products.find_one({'_id':itemId}) 
   form = formDict[item['type']](data=item)

   return render_template('updateItem.html', title='Update item', form=form, itemId=itemId)


@current_app.route('/inventory/search', methods = ['GET', 'POST'])
def searchInventory():
    form = SearchInventoryForm()
    if form.validate_on_submit():
        if form.searchField.data=='code':
            value = (form.searchValue.data).upper().replace(' ', '')+'$'
            query = {form.searchField.data:{'$regex':value}}
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
    mainQuery = json.loads(request.args.get('query').replace("'", "\""))
    items = listOfSearchedItems(mainQuery)
    
    if request.method == 'GET':
        for it in items:
            item = dict(zip(('id_', 'code', 'room', 'location',
                             'stocked_date', 'quantity'), 
                        (it['_id'], it['code'], it['room'],
                         it['location'], it['stocked_date'].strftime('%Y-%m-%d'),
                         it['quantity'])
                            )
                        )
            form.items.append_entry(item)

    if form.validate_on_submit():
        for litem, fitem in zip(items, form.items):
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
        
        return redirect(url_for('inventory', query=mainQuery))
    
    return render_template('inventory.html', title='Search result',
                           form=form)


@current_app.route('/item/view/<itemId>', methods = ['GET', 'POST'])
def viewItem(itemId):
    product = mongo.db.products.find_one({'_id':itemId})
    print(product)
    id = product.pop('_id')
    return render_template('viewItem.html', title='Item', product=product, id=id)


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
    if product['documentation']:
        mongo.db.products.update_one({'_id':itemId}, {'$set':{'documentation':product['documentation']}})
    else:
        mongo.db.products.update_one({'_id':itemId}, {'$unset':{'documentation':1}})
    
    return redirect(url_for('updateItem', itemId=itemId))
 

