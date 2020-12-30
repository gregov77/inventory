from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import mongo, bcrypt
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route('/', methods = ['GET', 'POST'])
@users.route('/index', methods = ['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_db = mongo.db.user.find_one({'username':username})
        if user_db and bcrypt.check_password_hash(user_db['password'], password):
            user = User(id=user_db['_id'], username=user_db['username'], password=user_db['password'])
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful', 'success')

            return redirect(next_page) if next_page else redirect(url_for('invtory.main'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash('You are logged out', 'info')
    return redirect(url_for('users.index'))

