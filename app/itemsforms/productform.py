from flask_wtf import FlaskForm
from wtforms import (StringField, FloatField, SubmitField,
                     TextAreaField, MultipleFileField, RadioField)
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    '''
        Parent form for all products.
    '''
     
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    part_number = StringField('Part number', validators=[DataRequired()])
    price = FloatField('Price')
    currency = RadioField('Currency', choices=[('GBP','£'), ('EUR','€'), ('USD','$')], default='GBP')
    dimension_unit = RadioField('Dimension unit', choices=[('MM','mm'), ('IN','in')], default='MM')
    description = TextAreaField('Description', validators=[DataRequired()])
    documentation = MultipleFileField('Documentation files')
    submit = SubmitField('Submit')