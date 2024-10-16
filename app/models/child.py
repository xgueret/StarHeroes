"""module du model Child"""
from app import db

class Child(db.Model):
    """class Child"""
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    ratings = db.relationship('Rating', back_populates='child', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Child(id={self.id}, name={self.name})>"
