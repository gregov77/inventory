from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, HiddenField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class AddItemForm(FlaskForm):
    '''
        Generic form displayed to add item to database from 
        the newItem page.
    
    Note:
        parameters should match Product class in models
    '''
    group_choices = [('mirror', 'mirror'), ('stage', 'stage')]
    
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    part_number = StringField('Part number', validators=[DataRequired()])
    group = SelectField('Type', choices=group_choices, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')   


class SearchInventoryForm(FlaskForm):
    '''
        Class defining the search form for the searchItem page.
    '''
    search_choices = [('code', 'part number'),
                      ('room', 'room'),
                      ('location', 'location')]
    
    searchField = SelectField('Search by:', choices=search_choices)
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
    code = StringField('Code', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    location = StringField('Room', validators=[DataRequired()])
    stocked_date = StringField('Room', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    

class SearchedItemListForm(FlaskForm):
    '''
        Form consisting of a list of SearchItemForm. This is the form
        that is passed to the searchItem page to display the found
        items.
    '''
    items = FieldList(FormField(SearchedItemForm))
    submit = SubmitField('Update')



