from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import mongo
import gridfs
from app.forms import StoreForm, SearchInventoryForm, formDict
from app.models import InStock
from app.select_lists import choices
from app.func_helpers import get_productDict, update_productDict, get_roomList, get_storageList
from flask_login import login_required

fs = gridfs.GridFS(mongo.db)

item = Blueprint('item', __name__)


@item.route('/item/new', methods = ['GET', 'POST'])
@login_required
def newItem():
    form = SearchInventoryForm()

    if form.is_submitted():
        group = form.searchType.data
        subgroup = form.searchSubtype.data.upper()
        return redirect(url_for('item.newItemEntry', group=group, subgroup=subgroup))
    
    return render_template('newItem.html', form=form, choices=choices)


@item.route('/item/new/<group>/<subgroup>', methods = ['GET', 'POST'])
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
            if docs:
                if docs[0].filename!='':
                    newProduct['documentation'] = dict()
                    for doc in docs:
                        uid = fs.put(doc, filename=doc.filename)
                        newProduct['documentation'][str(uid)]=doc.filename

            mongo.db.products.insert_one(newProduct)
            flash(f'Item added: {newProduct["_id"]}', 'success')
        
            return redirect(url_for('item.viewItem', itemId=newProduct['_id']))

    return render_template('newItemEntry.html', group=group, subgroup=subgroup, form=form, html_form=f'forms/{subgroup}.html')    


@item.route('/item/update/<itemId>', methods= ['GET', 'POST'])
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
            if itemDoc is None:
                updateDict['documentation'] = dict()
            else:
                updateDict['documentation'] = itemDoc
            for doc in docs:
                uid = fs.put(doc, filename=doc.filename)
                updateDict['documentation'][str(uid)]=doc.filename
        if len(updateDict)>0:
            mongo.db.products.update_one({'_id':itemId},
                                         {'$set':updateDict}, upsert=True)
        return redirect(url_for('item.viewItem', itemId=itemId))

    return render_template('updateItem.html', title=f'Update {itemId}',
                           form=form, itemId=itemId, itemDoc=itemDoc, html_form=f'forms/{item["type"]}.html')


@item.route('/item/view/<itemId>', methods = ['GET', 'POST'])
@login_required
def viewItem(itemId):
    product = mongo.db.products.find_one({'_id':itemId})
    id = product.pop('_id')
    return render_template('viewItem.html', title=id, product=product, id=id)


@item.route('/item/store/<itemId>', methods=['GET', 'POST'])
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

    return render_template('storeItem.html', form=form, itemId=itemId)


@item.route('/item/delete/<itemId>', methods= ['GET', 'POST'])
@login_required
def deleteItem(itemId):
    mongo.db.products.delete_one({'_id':itemId})
    flash(f'Item {itemId} removed from database.', 'info')
    return redirect(url_for('invtory.main'))