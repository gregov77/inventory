from flask import redirect, url_for, request, send_file, Blueprint, jsonify, app
from app import mongo
import gridfs
from bson import ObjectId
import json
from app.select_lists import get_search_fields
from flask_login import login_required

fs = gridfs.GridFS(mongo.db)

utils = Blueprint('utils', __name__)


@utils.route("/uploads/<string:id>")
@login_required
def get_upload(id):
    fin = fs.find_one({'_id':ObjectId(id)})
    data = fin.read()
    fext = fin.filename[-4:]
    tmpfile = '/home/gregory/temp/'+'tmpfile'+fext
    with open(tmpfile, 'wb') as fout:
        fout.write(data)
    
    return send_file(tmpfile)


@utils.route('/delete/<string:itemId>/<string:docId>')
@login_required
def delete_document(itemId, docId):
    fs.delete(ObjectId(docId))
    product = mongo.db.products.find_one({'_id':itemId})
    product['documentation'].pop(docId)
    if len(product['documentation'])>0:
        mongo.db.products.update_one({'_id':itemId}, {'$set':{'documentation':product['documentation']}})
    else:
        mongo.db.products.update_one({'_id':itemId}, {'$unset':{'documentation':1}})
    
    return redirect(url_for('item.updateItem', itemId=itemId))
 

@utils.route('/get_searchfield', methods=['GET', 'POST'])
@login_required
def get_searchfield():
    selection = request.args.get('selection').lower()
    try:
        dict_fields = dict(get_search_fields['base'], **get_search_fields[selection])
    except KeyError:
        dict_fields = get_search_fields['base']

    return jsonify(result=dict_fields)