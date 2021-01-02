from .productform import ProductForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired
from ..select_lists import coating_choices, crystal_material_choices

class CrystalForm(ProductForm):
    '''
        Crystal form.
    '''
        
    width = FloatField('Width')
    height = FloatField('Height')
    thickness = FloatField('Thickness')
    material = SelectField('Material', choices=crystal_material_choices)
    coating = SelectField('Coating', choices=coating_choices)