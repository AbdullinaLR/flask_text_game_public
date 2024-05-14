# import os
#
# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///characters.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
#
# class ProductionConfig(Config):
#     DEBUG = False
#     TESTING = False
#     # Other production-specific settings
#
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///characters.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
