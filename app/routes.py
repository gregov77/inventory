from flask import render_template, flash, redirect, url_for, request
from app import app, mongo
from .forms import AddedItemForm, SearchedItemForm, SearchedItemListForm, SearchForm
from .models import Optics
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
    results = mongo.db.optics.find(query)
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
        optics = Optics(part_number=form.part_number.data, 
                        quantity=form.quantity.data)
        mongo.db.optics.insert_one(optics.__dict__)
        flash(f'Item added: {optics.__dict__}')
        return redirect(url_for('newItem'))
    
    return render_template('newItem.html', title='Add item', form=form)


@app.route('/item/search', methods = ['GET', 'POST'])
def searchItem():
    form = SearchForm()
    if form.validate_on_submit():
        query = {form.searchField.data:form.searchValue.data}
        return redirect(url_for('foundItem', query=query))

    return render_template('searchItem.html', title='Search item',
                           form=form)


@app.route('/item/result', methods = ['GET', 'POST'])
def foundItem():
    form = SearchedItemListForm()
    mainQuery = json.loads(request.args.get('query').replace("'", "\""))
    items = listOfSearchedItems(mainQuery)
    
    if request.method == 'GET':
        for it in items:
            item = dict(zip(('id_', 'part_number', 'quantity'), 
                        (str(it['_id']), it['part_number'], it['quantity'])))
            form.items.append_entry(item)

    if request.method == 'POST':
        for litem, fitem in zip(items, form.items):
            if litem['quantity']  != fitem.quantity.data:
                query = { '_id': litem['_id'] }
                newvalues = { '$set': { 'quantity': fitem.quantity.data } }
                mongo.db.optics.update_one(query, newvalues)
                flash(f'Item changed: {litem["_id"]} {fitem.quantity.data}')
        
        return redirect(url_for('foundItem', query=mainQuery))
    
    return render_template('foundItem.html', title='Search result',
                           form=form)


@app.route('/item/update/<itemId>', methods = ['GET', 'POST'])
def updateItem(itemId):

    return render_template('updateItem.html', title='Update item')
