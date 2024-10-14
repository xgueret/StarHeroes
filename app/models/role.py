"""Module du model role"""
from app import db

class Role(db.Model):
    """Modèle pour la gestion des rôles"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False) # Ex: Admin", "parent"
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"


def init_roles():
    """Crée les rôles par défaut s'ils n'existent pas"""
    roles = ['admin', 'parent']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            new_role = Role(name=role_name)
            db.session.add(new_role)
    db.session.commit()
