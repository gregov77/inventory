from flask import render_template, flash, redirect, url_for, request
from app import app, mongo
from .forms import (AddedItemForm, SearchedItemForm, SearchedItemListForm,
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
    results = mongo.db.stock.find(query).sort('_id')
    items = [result for result in results]    
    
    return items

#
# VIEWS 
#
@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/item/new', methods = ['GET', 'POST'])
def newItem():
    form = AddedItemForm()
    if form.validate_on_submit():
        NewProduct = Product(part_number=form.part_number.data, 
                        quantity=form.quantity.data)
        mongo.db.products.insert_one(NewProduct.__dict__)
        flash(f'Item added: {NewProduct.__dict__}')
        return redirect(url_for('newItem'))
    
    return render_template('newItem.html', title='Add item', form=form)


@app.route('/inventory/search', methods = ['GET', 'POST'])
def searchInventory():
    form = SearchInventoryForm()
    if form.validate_on_submit():
        query = {form.searchField.data:form.searchValue.data}
        return redirect(url_for('inventory', query=query))

    return render_template('searchInventory.html', title='Search item',
                           form=form)


@app.route('/inventory', methods = ['GET', 'POST'])
def inventory():
    form = SearchedItemListForm()
    mainQuery = json.loads(request.args.get('query').replace("'", "\""))
    items = listOfSearchedItems(mainQuery)
    
    if request.method == 'GET':
        for it in items:
            item = dict(zip(('id_', 'part_number', 'quantity'), 
                        (str(it['_id']), it['part_number'], it['quantity'])))
            form.items.append_entry(item)

    if request.method=='POST':
        for litem, fitem in zip(items, form.items):
            quantity = fitem.quantity.data
            if isinstance(quantity, int) and quantity >= 0:
                query = { '_id': litem['_id'] }
                if quantity == 0:
                    mongo.db.stock.delete_one(query)
                    flash(f'Item removed: {litem["_id"]} {fitem.id_.data}.')
                if litem['quantity']  != quantity:
                    newvalues = { '$set': { 'quantity': quantity } }
                    mongo.db.stock.update_one(query, newvalues)
                    flash(f'Item changed: {litem["_id"]} {quantity}.')
            else:
                flash(f'Quantity for item {litem["_id"]} should be an integer.')
        
        return redirect(url_for('inventory', query=mainQuery))
    
    return render_template('inventory.html', title='Search result',
                           form=form)


@app.route('/item/<itemId>', methods = ['GET', 'POST'])
def viewItem(itemId):

    return render_template('viewItem.html', title='Update item')
