import os


class Config:
    SECRET_KEY = 'you-will-never-guess'
    MONGO_URI = 'mongodb://localhost:27017/test'


class Config_test:
    SECRET_KEY = 'you-will-never-guess'
    MONGO_URI = 'mongodb://localhost:27017/test'
    TESTING = True
    WTF_CSRF_ENABLED = False    