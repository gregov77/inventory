from flask import render_template, flash, redirect, url_for, request
from flask import current_app
from app import mongo
from .forms import (AddItemForm, SearchedItemForm, SearchedItemListForm,
    SearchInventoryForm)
from .models import Product, InStock
from bson import ObjectId
import json


#
# FUNCTIONS
#
def listOfSearchedItems(query):
    '''
        return list of queried items from initial search
        in the searchItem view.

    Args:
        query(dict): dictionnary returned by the searchItem view as query
    
    Returns:
        items(list): list of documents (as dict) 
    '''
    results = mongo.db.instock.find(query).sort('_id')
    items = [result for result in results]    
    
    return items

#
# VIEWS 
#
@current_app.route('/')
@current_app.route('/index')
def index():
    return render_template('base.html')


@current_app.route('/item/new', methods = ['GET', 'POST'])
def newItem():
    form = AddItemForm()
    if form.validate_on_submit():
        NewProduct = Product(manufacturer=form.manufacturer.data,
                             part_number=form.part_number.data,
                             group = form.group.data, 
                             price = form.price.data,
                             description = form.description.data)
        checkNewProduct = mongo.db.products.find_one({'_id':NewProduct._id})
        if checkNewProduct:
            flash(u'Item already in the database.')
        else:
            mongo.db.products.insert_one(NewProduct.__dict__)
            flash(f'Item added: {NewProduct.__dict__}')
        return redirect(url_for('newItem'))
    
    return render_template('newItem.html', title='Add item', form=form)


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

    if request.method=='POST':
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


@current_app.route('/item/<itemId>', methods = ['GET', 'POST'])
def viewItem(itemId):
    product = mongo.db.products.find_one({'_id':itemId})
    print(product)
    return render_template('viewItem.html', title='Item', product=product)
