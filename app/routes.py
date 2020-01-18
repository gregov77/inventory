from flask import render_template, flash, redirect, url_for, request
from app import app, mongo
from .forms import OpticsForm, SearchForm
from .models import Optics


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/newItem', methods = ['GET', 'POST'])
def newItem():
    form = OpticsForm()
    if form.validate_on_submit():
        optics = Optics(part_number=form.part_number.data, 
                        quantity=form.quantity.data)
        mongo.db.optics.insert_one(optics.__dict__)
        flash(f'Item added: {optics.__dict__}')
        return redirect('/newItem')
    return render_template('newItem.html', title='Add item', form=form)


@app.route('/searchItem', methods = ['GET', 'POST'])
def searchItem():
    form = SearchForm()
    results = None
    if form.validate_on_submit():
        searchfield = form.searchField.data
        searchvalue = form.searchValue.data
        results = mongo.db.optics.find({searchfield:searchvalue})
    return render_template('searchItem.html', title='Search item', form=form, results=results)