"""module du model Rule"""
from app import db

class Rule(db.Model):
    """class Rule"""
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    ratings = db.relationship('Rating', back_populates='rule', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Rule(id={self.id}, name={self.name}, description={self.description})>"
