from .models import Optics
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class OpticsForm(FlaskForm):
    part_number = StringField('Part number', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    searchField = SelectField(u'Search by:', choices=[('part_number', 'part number')])
    searchValue = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')
