from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


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




