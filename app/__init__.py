from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)

print('Ole')

from app import routes