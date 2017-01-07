import os


REDIS_PORT = '6489'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    REDISTOGO_URL = os.getenv('REDISTOGO_URL')
    SECRET_KEY = 'change-this-asap'
    AMPLITUDE_KEY = os.getenv('AMPLITUDE_KEY')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    CUSTOMER_IO_SITE_ID = ''
    CUSTOMER_IO_API_KEY = ''


class ProductionConfig(Config):
    CUSTOMER_IO_SITE_ID = ''
    CUSTOMER_IO_API_KEY = ''