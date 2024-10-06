"""module du model Rating"""
from app import db

class Rating(db.Model):
    """class Rating"""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    stars = db.Column(db.Integer, nullable=False, check_constraint='stars >= 0 AND stars <= 2')
    
    # Relations
    child = db.relationship('Child', backref='ratings')
    rule = db.relationship('Rule', backref='ratings')
