from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config
from os import getcwd


mongo = PyMongo()
login_manager = LoginManager()
bcrypt = Bcrypt()
ROOT = getcwd()
TMP = ROOT +'/tmp/'

def create_app(config_class=Config):
    ''' Initialise the core application.'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialise plugins
    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.users.routes import users
    from app.item.routes import item
    from app.invtory.routes import invtory
    from app.utils.routes import utils
    app.register_blueprint(users)
    app.register_blueprint(item)
    app.register_blueprint(invtory)
    app.register_blueprint(utils)
    
    return app