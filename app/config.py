import os


class Config:
    SECRET_KEY = 'you-will-never-guess'
    MONGO_URI = 'mongodb://localhost:27017/test'
    TMP = '/home/gregory/temp/'


class Config_test:
    SECRET_KEY = 'you-will-never-guess'
    MONGO_URI = 'mongodb://localhost:27017/test'
    TMP = '/home/gregory/temp/'
    TESTING = True
    WTF_CSRF_ENABLED = False    