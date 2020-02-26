from app import mongo
import json

formFieldOnly = ['submit', 'csrf_token', 'documentation']

def get_products_and_stocks(query):
    '''
        return list of queried items from initial search
        in the searchItem view.

    Args:
        query(dict): dictionnary returned by the searchItem view as query
    
    Returns:
        products(list): list of product documents (as dict) matching the query
        stocks(list): list of stocks (as dict) matching the query 
    '''
    productList = mongo.db.products.find(query, {'_id':1, 'type':1})
    products = [product for product in productList]
    distinctProductId = list({product['_id'] for product in products})
    stockQuery = {'code':{'$in':distinctProductId}}
    stockList = mongo.db.instock.find(stockQuery).sort('_id')
    stocks = [stock for stock in stockList]    
    
    return products, stocks


def get_productDict(subgroup, dict_):
    '''
        Produce a dictionnary used to instantiate a Product.

    Args:
        subgroup(str): subtype of object as string
        dict_(dict): dictionnary of keys/values from form data
    
    Returns:
        productDict(dict): dictionnary for object instantiation
    '''
    productDict = dict(type=subgroup.upper())
    for k, v in dict_.items():
        if k not in formFieldOnly+'description':
            if isinstance(v, str): v = v.upper() 
            productDict[k] = v
    productDict['_id'] = productDict['manufacturer']+'-'+productDict['part_number']

    return productDict


def update_productDict(productId, dataDict):
    '''
        Produce a dictionnary used to update a Product.

    Args:
        product(str): key _id of the product to update
        dataDict(dict): dictionnary of keys/values from form data
    
    Returns:
        productDict(dict): dictionnary of changed keys/values
    '''
    productDict = dict()
    product = mongo.db.products.find_one({'_id':productId})
    for k, v in dataDict.items():
        if k not in formFieldOnly:
            if product[k] != v: productDict[k] = v

    print(productDict)
    return productDict


def set_roomList():
    '''
        Produce a list of tuples to fill Locations.roomList.choices
        from file locations.json.

    Args:
     
    Returns:
        room_list(list): list of rooms as [(room_i, room_i), ...]
    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    room_list = [(k, k) for k in locations.keys()]

    return room_list


def set_storageList(room):
    '''
        Produce a list of tuples to fill Locations.storageList.choices
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
        Add room name to locations.json

    Args:
        room(str): string returned from Locations.room.data
    
    Returns:
        room(str): cleaned room arg with upper letter an removed white spaces
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
        Add storage name to locations.json

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
        Delete room name from locations.json

    Args:
        room(str): string returned from Locations.roomList.data
    
    Returns:

    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    
    locations.pop(room)
    
    with open('app/locations.json', 'w') as fd:
        json.dump(locations, fd)


def delete_storage(room, storage):
    '''
        Delete storage name from locations.json

    Args:
        room(str): string returned from Locations.roomList.data
        storage(str): string returned from Locations.storageList.data
    
    Returns:

    '''
    with open('app/locations.json', 'r') as fd:
        locations = json.load(fd)
    
    locations[room].remove(storage)
    
    with open('app/locations.json', 'w') as fd:
        json.dump(locations, fd)