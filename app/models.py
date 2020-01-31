class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Product:
    def __init__(self, id_=None, part_number=None, group=None, quantity=None):
        self.id_ = id_
        self.part_number = part_number
        self.group = group 
        self.quantity = quantity

class InStock:
    def __init__(self, id_=None, part_number=None, quantity=None, 
                 room=None, location=None):
        self.id_ = id_
        self.part_number = part_number
        self.quantity = quantity
        self.room = room
        self.location = location
        




