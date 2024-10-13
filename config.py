""" config.py """
import secrets

class Config:
    """Config"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SECRET_KEY = secrets.token_urlsafe(32)
    HOST = '127.0.0.1'
    PORT = 5000

class ProductionConfig(Config):
    """Production config"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 8000

class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
