from flask import Flask
from flask_mongoengine import MongoEngine
db = MongoEngine()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db':'test'
}
app.config['SECRET_KEY'] = 'you-will-never-guess'
db.init_app(app)

from app import routes