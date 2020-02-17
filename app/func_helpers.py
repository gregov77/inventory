from app import mongo

formFieldOnly = ['submit', 'csrf_token', 'documentation']

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


def createProductDict(subgroup, dict_):
    '''
        Produce a dictionnary used to instantiate a Product.

    Args:
        group(str): main type of object as string
        subgroup(str): subtype of object as string
        dict_(dict): dictionnary of keys/values from form data
    
    Returns
        productDict(dict): dictionnary for object instantiation
    '''
    productDict = dict(type=subgroup.upper())
    for k, v in dict_.items():
        if k not in formFieldOnly:
            if isinstance(v, str): v = v.upper() 
            productDict[k] = v
    productDict['_id'] = productDict['manufacturer']+'-'+productDict['part_number']

    return productDict


def updateProductDict(productId, dataDict):
    '''
        Produce a dictionnary used to update a Product.

    Args:
        product(str): key _id of the product to update
        dataDict(dict): dictionnary of keys/values from form data
    
    Returns
        productDict(dict): dictionnary of changed keys/values
    '''
    productDict = dict()
    product = mongo.db.products.find_one({'_id':productId})
    for k, v in dataDict.items():
        if k not in formFieldOnly:
            if product[k] != v: productDict[k] = v

    print(productDict)
    return productDict

    
