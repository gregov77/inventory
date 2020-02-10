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


# class Product:
#     def __init__(self, manufacturer, part_number, group, subgroup, price, description):
#         self.manufacturer = manufacturer.upper()
#         self.part_number = part_number.upper()
#         self._id = self.manufacturer[:3]+'-'+self.part_number
#         self.group = group.upper()
#         self.subgroup = subgroup.upper()
#         self.price = price
#         self.description = description


# class Mirror(Product):
#     diameter = None
#     coating = None
#     curvature = None

#     def __init__(self, manufacturer, part_number, group, subgroup, price, description,
#                  diameter, coating, curvature):
#         super().__init__(manufacturer, part_number, group, price, description)
#         self.diameter = diameter
#         self.coating = coating
#         self.curvature = curvature


class InStock:
    def __init__(self, id_=None, code=None, quantity=None, 
                 room=None, location=None):
        self.code = code.upper()
        self.quantity = int(quantity)
        self.room = room.upper()
        self.location = location.upper()
        self.stocked_date = datetime.utcnow()




