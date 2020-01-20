from .models import Optics
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, HiddenField, FormField, FieldList
from wtforms.validators import DataRequired

class AddedItemForm(FlaskForm):
    '''
        Generic form displayed to add item to database from 
        the newItem page.
    '''
    part_number = StringField('Part number', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()]) 
    submit = SubmitField('Submit')   


class SearchedItemForm(FlaskForm):
    '''
        Generic form for a single item returned from a search
        in the searchItem page.

    Note:
        This class forms the building block of the class SearchedItemListForm. 
    '''
    _id = HiddenField('id', validators=[DataRequired()])
    part_number = StringField('Part number', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])


class SearchedItemListForm(FlaskForm):
    '''
        Form consisting of a list of SearchItemForm. This is the form
        that is passed to the searchItem page to display the found
        items.
    '''
    items = FieldList(FormField(SearchedItemForm))
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    '''
        Class defining the search form for the searchItem page.
    '''
    searchField = SelectField(u'Search by:', choices=[('part_number', 'part number')])
    searchValue = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')
