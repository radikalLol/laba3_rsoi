# /src/config.py

import os

class Development(object):

    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'hhgaghhgsdhdhdd'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
class Production(object):

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'hhgaghhgsdhdhdd'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app_config = {
    'development': Development,
    'production': Production,
}
