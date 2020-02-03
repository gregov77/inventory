from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Product:
    def __init__(self, manufacturer, part_number, group, description):
        self.manufacturer = manufacturer.upper()
        self.part_number = part_number.upper()
        self._id = self.manufacturer[:3]+'-'+self.part_number
        self.group = group.upper() 
        self.description = description

class InStock:
    def __init__(self, id_=None, part_number=None, quantity=None, 
                 room=None, location=None):
        self.id_ = id_
        self.part_number = part_number
        self.quantity = quantity
        self.room = room
        self.location = location
        self.stocked_date = datetime.utcnow()




