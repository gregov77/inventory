from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


mongo = PyMongo()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    ''' Initialise the core application.'''
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config["MONGO_URI"] = 'mongodb://localhost:27017/test'
    app.config["TMP"] = '/home/gregory/temp/'

    # Initialise plugins
    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from app import routes

        return app