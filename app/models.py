import mongoengine as me


class Optics(me.Document):
    part_number = me.StringField(required=True)
    quantity = me.IntField(required=True)



