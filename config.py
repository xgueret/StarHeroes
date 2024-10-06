""" config.py """
import secrets

class Config:
    """Config"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SECRET_KEY = secrets.token_urlsafe(32)
    
class ProductionConfig(Config):
    """Production config"""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True
