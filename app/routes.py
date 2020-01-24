from flask import render_template, flash, redirect, url_for, request
from app import app, mongo
from .forms import AddedItemForm, SearchedItemForm, SearchedItemListForm, SearchForm
from .models import Optics
from bson.objectid import ObjectId


#
# FUNCTIONS
#
def listOfSearchedItems(query):
    '''
        return list of queried items from initial search
        in the searchItem view.

    Args:
        form(SearchForm): form returned by the searchItem view
    
    Returns:
        items(SearchedItemForm): form containing returned items
        pnList: list of part numbers of returned items
    '''
    items = SearchedItemListForm()
    pnList = []
    
    results = mongo.db.optics.find(query)
        
    for result in results:
        item = SearchedItemForm()
        item.id_.data = str(result['_id'])
        item.part_number.data = result['part_number']
        item.quantity.data = result['quantity']
        pnList.append(result['part_number'])
        items.items.append_entry(item)
    
    return items, pnList

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
        return redirect('/newItem')
    
    return render_template('newItem.html', title='Add item', form=form)


@app.route('/item/search', methods = ['GET', 'POST'])
def searchItem():
    form = SearchForm()

    # for item in items.items.entries:
    #     print(item.data['quantity'])
    #     query = { '_id': ObjectId(item.id_.data) }
    #     newvalues = { '$set': { 'quantity': item.quantity.data } }
    #     mongo.db.optics.update_one(query, newvalues)

    #     items, pnList = listOfSearchedItems(form)

    return render_template('searchItem.html', title='Search item',
                           form=form)


@app.route('/item/result', methods = ['GET', 'POST'])
def foundItem():
    query = {request.form.searchField:request.form.searchValue}
    items, pnList = listOfSearchedItems(query)

    return render_template('foundtitem.html', title='Search result',
                           items=items, pnList=pnList)           