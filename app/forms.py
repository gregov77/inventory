from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, FloatField, SubmitField,
                     SelectField, HiddenField, FormField, FieldList,
                     TextAreaField, MultipleFileField)
from wtforms.validators import DataRequired, ValidationError, InputRequired
from .select_lists import type_choices, optics_choices, coating_choices


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


class ProductForm(FlaskForm):
    '''
        Parent form for all products.
    '''
     
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    part_number = StringField('Part number', validators=[DataRequired()])
    price = FloatField('Last price')
    description = TextAreaField('Description', validators=[DataRequired()])
    documentation = MultipleFileField('Documentation files')
    submit = SubmitField('Submit')


class MirrorForm(ProductForm):
    '''
        Parent form for all products.
    '''
     
    diameter = FloatField('Diameter', validators=[DataRequired()])
    coating = SelectField('Coating', choices=coating_choices, validators=[DataRequired()])
    curvature = FloatField('Curvature', validators=[DataRequired()])
    

class SearchInventoryForm(FlaskForm):
    '''
        Class defining the search form for the searchItem page.
    '''
    search_choices = [('part_number', 'part number'),
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
    roomList = SelectField('Room list', coerce=str)
    viewStorage = SubmitField('View locations')
    delete_room = SubmitField('Delete')
    storage = StringField('Storage')
    addStorage = SubmitField('Add')
    storageList = SelectField('Storage list', coerce=str)
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


formDict = {'MIRRORS':MirrorForm}



