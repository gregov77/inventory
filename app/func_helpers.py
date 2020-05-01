from app import mongo
import json
from .select_lists import non_str_fields

formFieldOnly = ['submit', 'csrf_token', 'documentation']

def set_query(group, fields, values):
    '''
        Function creating the query used to search the database.
        Arguments are obtained from the SearchInventoryForm form from the searchInventory route.

    Args:
        group(str): group to which the product belong (mirror, window, stage, etc.)
        fields(str): search fields (linked from database keys) from select list
        values(str): search values entered by the user in teh SearchInventoryForm form
    
    Returns:
        query(str): query for mongoDB in string form.
    '''
    query_list = [{'type':group}]
    for field, value in zip(fields, values):
        if value!='':
            if field in non_str_fields['float']:
                query_list.append({ field:float(value) })
            elif field == 'part_number':
                value = value.upper().replace(' ', '')
                query_list.append({ "part_number":{"$regex":f'.*{value}.*'} })
            else:
                value = value.replace(' ','')
                query_list.append({ field:value })

    query = {'$and':query_list}
    return f'{query}'


def get_products_and_stocks(query):
    '''
        Function returning list of queried products and stocks from initial search
        in the searchInventory view.

    Args:
        query(dict): dictionnary from the query string returned by the set_query function
    
    Returns:
        products(list): list of product documents (as dict) matching the query
        stocks(list): list of stocks (as dict) matching the query 
    '''
    productList = mongo.db.products.find(query, {'_id':1, 'type':1})
    products = [product for product in productList]
    distinctProductId = list({product['_id'] for product in products})
    stockQuery = {'code':{'$in':distinctProductId}}
    # Stock list sorted by _id values to get same order on each call (for updates)
    stockList = mongo.db.instock.find(stockQuery).sort('_id')
    stocks = [stock for stock in stockList]    
    
    return products, stocks


def get_productDict(subgroup, dict_):
    '''
        Function returning a dictionnary used to instantiate a Product.

    Args:
        subgroup(str): subtype of object as string (mirror, window, stage, etc.)
        dict_(dict): dictionnary of keys/values from formDict data from newItemEntry route
    
    Returns:
        productDict(dict): dictionnary for object instantiation
    '''
    productDict = dict(type=subgroup.upper())
    for k, v in dict_.items():
        if k not in formFieldOnly+['description']:
            if isinstance(v, str): v = v.upper() 
            productDict[k] = v
    productDict['_id'] = productDict['manufacturer']+'-'+productDict['part_number']
    productDict['description'] = dict_['description']

    return productDict


def update_productDict(productId, dataDict):
    '''
        Function returning a dictionnary of keys/values to update in a product.

    Args:
        productId(str): key _id of the product to update
        dataDict(dict): dictionnary of keys/values from formDict data
    
    Returns:
        productDict(dict): dictionnary of changed keys/values
    '''
    productDict = dict()
    product = mongo.db.products.find_one({'_id':productId})
    for k, v in dataDict.items():
        if k not in formFieldOnly:
            if product.get(k) is None and v!='':
                productDict[k] = v 
            elif product.get(k) is not None and product[k] != v: 
                productDict[k] = v

    print(productDict)
    return productDict


def get_roomList():
    '''
        Function returning a list of tuples to fill Locations.roomList.choices
        from file locations.json.

    Args:
        No argument
        
    Returns:
        room_list(list): list of rooms as [(room_i, room_i), ...]
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    room_list = [(k, k) for k in locations.keys()]

    return room_list


def get_storageList(room):
    '''
        Function returning a list of tuples to fill Locations.storageList.choices
        from file locations.json.

    Args:
        room(str): room name used as key to retrieve storages from that room
    
    Returns:
        storage_list(list): list of rooms as [(storage_i, storage_i), ...]
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    storage_list = [(v, v) for v in locations[room]]

    return storage_list


def save_room(room):
    '''
        Function that adds room name to locations.json

    Args:
        room(str): string returned from Locations.room.data
    
    Returns:
        room(str): cleaned room arg with upper letter and removed white spaces
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    room = room.upper().replace(' ', '')
    if room not in locations.keys():
        locations[room] = ['']
        with open('app/locations.json', 'w') as fd:
            json.dump(locations, fd)

    return room


def save_storage(room, storage):
    '''
        Function that adds storage name to locations.json

    Args:
        room(str): string returned from Locations.roomList.data
        storage(str): string returned from Locations.storage.data
    
    Returns:
        storage(str): cleaned storage name
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    storage = ' '.join(storage.upper().split())
    if storage not in locations[room]:
        locations[room].append(storage)
        print(room, locations[room])
    with open('app/locations.json', 'w') as fd:
        json.dump(locations, fd)
    
    return storage


def delete_room(room):
    '''
        Function that deletes room name from locations.json

    Args:
        room(str): string returned from Locations.roomList.data
    
    Returns:
        No return
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    
    locations.pop(room)
    
    with open('app/locations.json', 'w') as fd:
        json.dump(locations, fd)


def delete_storage(room, storage):
    '''
        Function that deletes storage name from locations.json

    Args:
        room(str): string returned from Locations.roomList.data
        storage(str): string returned from Locations.storageList.data
    
    Returns:
        No return
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    
    locations[room].remove(storage)
    
    with open('app/locations.json', 'w') as fd:
        json.dump(locations, fd)