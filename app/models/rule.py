"""module du model Rule"""
from app import db

class Rule(db.Model):
    """class Rule"""
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.string(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
