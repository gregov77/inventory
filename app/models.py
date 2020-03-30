from datetime import datetime
from app import mongo, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.user.find_one({'_id':user_id})
    return User(user)


class User():
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


class Product:
    def __init__(self, dictionary):
        self.manufacturer = 'init'
        self.part_number = 'init'
        for k, v in dictionary.items():
            setattr(self, k, v)
        self._id = self.manufacturer[:3]+'-'+self.part_number


class InStock:
    def __init__(self, id_=None, code=None, quantity=None, 
                 room=None, storage=None):
        self.code = code
        self.quantity = quantity
        self.room = room
        self.storage = storage
        self.stocked_date = datetime.utcnow()




