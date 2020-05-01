from flask import render_template, flash, redirect, url_for, request, send_file, Blueprint
from flask import current_app, jsonify
from app import mongo
import gridfs
from app.forms import SearchedItemListForm, SearchInventoryForm, LocationsForm
import json
from app.select_lists import choices
from app.func_helpers import (get_products_and_stocks,
                           get_roomList, get_storageList, save_room, save_storage, delete_room,
                           delete_storage, set_query)
from flask_login import login_required

invtory = Blueprint('invtory', __name__)


@invtory.route('/main')
@login_required
def main():
    return render_template('main.html')


@invtory.route('/inventory/search', methods = ['GET', 'POST'])
@login_required
def searchInventory():
    form = SearchInventoryForm()
    if form.is_submitted():
        subtype = form.searchSubtype.data.upper()
        searchFields = [form.searchField1.data, form.searchField2.data, form.searchField3.data]
        searchValues = [form.searchValue1.data, form.searchValue2.data, form.searchValue3.data]
        query = set_query(subtype, searchFields, searchValues)

        return redirect(url_for('invtory.inventory', query=query))

    return render_template('searchInventory.html', title='Search inventory',
                           form=form, choices=choices)


@invtory.route('/inventory/<query>', methods = ['GET', 'POST'])
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
        
        return redirect(url_for('invtory.inventory', query=query))
    
    return render_template('inventory.html', title='Inventory', form=form, products=products, query=query)


@invtory.route('/locations', methods=['GET', 'POST'])
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

        return redirect(url_for('invtory.locations', roomDefault=roomDefault))
    
    if form.validate_on_submit() and form.addStorage.data:
        if form.storage.data !='':
            print(form.roomList.data, form.storage.data)
            newStorage = save_storage(form.roomList.data, form.storage.data)
            flash(f'storage {newStorage} added in room {form.roomList.data}.', 'info')
        else:
            flash('Provide a proper storage name as string.', 'danger')
        
        return redirect(url_for('invtory.locations', roomDefault=form.roomList.data))

    if form.validate_on_submit() and form.viewStorage.data:
        return redirect(url_for('invtory.locations', roomDefault=form.roomList.data))

    if form.validate_on_submit() and form.delete_room.data:
        delete_room(form.roomList.data)
        flash(f'Room {form.roomList.data} has been deleted.', 'info')
        
        return redirect(url_for('invtory.locations'))

    if form.validate_on_submit() and form.delete_storage.data:
        delete_storage(form.roomList.data, form.storageList.data)
        flash(f'Storage {form.storageList.data} has been deleted.', 'info')
        return redirect(url_for('invtory.locations', roomDefault=form.roomList.data))
    
    return render_template('locations.html', title='Locations', form=form)