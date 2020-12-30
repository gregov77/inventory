from .productform import ProductForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired
from ..select_lists import coating_choices

class MirrorForm(ProductForm):
    '''
        Mirror form.
    '''
     
    diameter = FloatField('Diameter')
    coating = SelectField('Coating', choices=coating_choices)
    focal_length = FloatField('Focal length')