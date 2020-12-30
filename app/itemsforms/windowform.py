from .productform import ProductForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired
from ..select_lists import coating_choices

class WindowForm(ProductForm):
    '''
        Window form.
    '''
        
    diameter = FloatField('Diameter', validators=[DataRequired()])
    thickness = FloatField('Thickness', validators=[DataRequired()])
    coating = SelectField('Coating', choices=coating_choices, validators=[DataRequired()])