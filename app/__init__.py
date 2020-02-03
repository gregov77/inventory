from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    ''' Initialise the core application.'''
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config["MONGO_URI"] = 'mongodb://localhost:27017/test'
    
    # Initialise plugins
    mongo.init_app(app)

    with app.app_context():
        from app import routes

        return app