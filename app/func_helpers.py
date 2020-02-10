from app import mongo

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


def createProductDict(group, subgroup, dict_):
    '''
        Produce a dictionnary used to instantiate a Product.

    Args:
        group(str): main type of object as string
        subgroup(str): subtype of object as string
        dict_(dict): dictionnary of keys/values from form data
    
    Returns
        productDict(dict): dictionnary for object instantiation
    '''
    productDict = dict(group=group.upper(), subgroup=subgroup.upper())
    for k, v in dict_.items():
        if k!='submit' and k!='csrf_token':
            if isinstance(v, str) and k!='description': v = v.upper() 
            productDict[k] = v
    productDict['_id'] = productDict['manufacturer']+'-'+productDict['part_number']
    
    return productDict