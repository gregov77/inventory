from .models import Optics
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, HiddenField, FormField, FieldList
from wtforms.validators import DataRequired, ValidationError

class AddedItemForm(FlaskForm):
    '''
        Generic form displayed to add item to database from 
        the newItem page.
    '''
    part_number = StringField('Part number', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()]) 
    submit = SubmitField('Submit')   


class SearchForm(FlaskForm):
    '''
        Class defining the search form for the searchItem page.
    '''
    searchField = SelectField(u'Search by:', choices=[('part_number', 'part number')])
    searchValue = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchedItemForm(FlaskForm):
    '''
        Generic form for a single item returned from a search
        in the searchItem page.

    Note:
        This class forms the building block of the class SearchedItemListForm. 
    '''
    id_ = HiddenField('id', validators=[DataRequired()])
    part_number = StringField('Part number', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])

    def validate_quantity(form, field):
        if not isinstance(field.data, int):
            raise ValidationError('Quantity must be an integer.')
        if field.data<0:
            raise ValidationError('Quantity must be a positive integer.')


class SearchedItemListForm(FlaskForm):
    '''
        Form consisting of a list of SearchItemForm. This is the form
        that is passed to the searchItem page to display the found
        items.
    '''
    items = FieldList(FormField(SearchedItemForm))
    submit = SubmitField('Update')



