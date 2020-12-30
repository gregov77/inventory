from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, FloatField, SubmitField,
                     SelectField, HiddenField, FormField, FieldList,
                     TextAreaField, MultipleFileField, PasswordField, RadioField)
from wtforms.validators import DataRequired, ValidationError, InputRequired
from .select_lists import type_choices, coating_choices, choices


class LoginForm(FlaskForm):
    '''
        Form to enter user name and password.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class NewTypeForm(FlaskForm):
    '''
        Form displayed to choose type of new item to add to database from 
        the newItem page.
    '''
    group = SelectField('Type:', choices=type_choices, validators=[InputRequired()])
    submit = SubmitField('Submit')


class NewSubTypeForm(FlaskForm):
    '''
        Form displayed to choose subtype of new item to add to database from 
        the newItem page.

    Note:
        SelectField uses dynamic choices depending on the initial type of product.
    '''
    subgroup = SelectField('Subtype:', coerce=str, validators=[InputRequired()])
    submit = SubmitField('Submit')


class SearchInventoryForm(FlaskForm):
    '''
        Class defining the search form for the searchItem page.
        Class also used for the newItem page.
    '''
    searchType = SelectField('', choices=list(zip(choices.keys(), choices.keys())), validators=[InputRequired()])
    searchSubtype = SelectField('', choices=[('None', 'choose a subtype')], validators=[InputRequired()])
    searchField1 = SelectField('', coerce=str, choices=[])
    searchValue1 = StringField('')
    searchField2 = SelectField('', coerce=str, choices=[])
    searchValue2 = StringField('')
    searchField3 = SelectField('', coerce=str, choices=[])
    searchValue3 = StringField('')
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
    storage = StringField('Storage', validators=[DataRequired()])
    stocked_date = StringField('Date', validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])


class SearchedItemListForm(FlaskForm):
    '''
        Form consisting of a list of SearchItemForm. This is the form
        that is passed to the searchItem page to display the found
        items.
    '''
    items = FieldList(FormField(SearchedItemForm))
    submit = SubmitField('Update')


class LocationsForm(FlaskForm):
    '''
        form to add/remove rooms and locations.
    '''
    room = StringField('Room')
    addRoom = SubmitField('Add')
    roomList = SelectField('Room', coerce=str)
    viewStorage = SubmitField('View room storage')
    delete_room = SubmitField('Delete')
    storage = StringField('Add storage')
    addStorage = SubmitField('Add')
    storageList = SelectField('Remove storage', coerce=str)
    delete_storage = SubmitField('Delete')


class StoreForm(FlaskForm):
    '''
        form to add item to inventory
    '''
    
    roomSelect = SelectField('Room', coerce=str, validators=[DataRequired()])
    roomSubmit = SubmitField('Select')
    storageSelect = SelectField('Storage', coerce=str)
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')

#================#
# All item forms #
#================#

from .itemsforms import *
