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
    app.config['TESTING'] = True

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