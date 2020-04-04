from datetime import datetime
from app import mongo, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.user.find_one({'_id':user_id})
    return User(user)


class User():
    '''
        Class to define user characteristics.

    Args:
        id(str, ObjectId): corresponds to user _id in mongoDB database
        username(str): user name
        password(str): user password

    Returns:
        Instance of user:
        is_active(property): True
        is_authenticated(property): True
        is_anonymous(property): False
        get_id(function): return user id
    '''
    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password
    
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


class InStock:
    '''
        Class defining an entry in the inventory stock.

    Args:
        id_(str, ObjectId): corresponds to stock _id in mongoDB database
        code(str): string made of the manufacturer and part number values to identify the product 
        quantity(int): quantity stocked
        room(str): room in which the products are stocked
        storage(str): place in which the products are stocked

    Returns:
        Instance of Instock with extra variable stocked_date(datetime.utcnow() as data/time of entry
        into the stock.
    '''
    def __init__(self, id_=None, code=None, quantity=None, 
                 room=None, storage=None):
        self.code = code
        self.quantity = quantity
        self.room = room
        self.storage = storage
        self.stocked_date = datetime.utcnow()