"""app/models.py"""
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    status   = db.Column(db.string(10), nullable=False, default='request') # Status: request, valid, rejected
    
    def set_password(self, password):
        """Hash and set password."""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check the password against the stored hash"""
        return check_password_hash(self.password, password)
    
class Child(db.Model):
    """Child model"""
    __tablename__ = 'children'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Rule(db.Model):
    """Rule model"""
    __tablename__ = 'rules'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    
class Rating(db.Model):
    """Rating model"""
    __tablename__ = 'ratings'
    id       = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    rule_id  = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=False)
    day      = db.Column(db.String(10), nullable=False) # stocke le jour sous forme de chaine de caractères (ex: 'Monday')
    stars    = db.Column(db.Integer, nullable=False) # Nombre d'étoiles (de 0 à 2)
    
    # Relations
    child = db.relationship('Child', backref='rating')
    rule = db.relationship('Rule', backref='ratings')
