"""module du moadel User"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model, UserMixin):
    """class User"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(20), default='request') # 'request', 'valid', 'rejected'
    
    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Verify if the password matches the hash."""
        return check_password_hash(self.password, password)
