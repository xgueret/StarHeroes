"""module du moadel User"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.role import Role

class User(db.Model, UserMixin):
    """class User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='request')

    __table_args__ = (
        db.CheckConstraint("status IN ('request', 'valid', 'rejected')", name='check_status_valid'),
    )

    # Relation avec les rôles via la table d'association UserRole
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, password={self.password}, status={self.status})>"

    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify if the password matches the hash."""
        return check_password_hash(self.password, password)

    def has_role(self, role_name):
        """Vérifie si un utilisateur a un rôle spécifique."""
        return any(role.name == role_name for role in self.roles)

    def add_role(self, role_name):
        """Ajoute un rôle à l'utilisateur."""
        role = Role.query.filter_by(name=role_name).first()
        if role and not self.has_role(role_name):
            self.roles.append(role)

    def remove_role(self, role_name):
        """Supprime un rôle à l'utilisateur."""
        role = Role.query.filter_by(name=role_name).first()
        if role and self.has_role(role_name):
            self.roles.remove(role)

    def set_status(self, new_status):
        """Set the status of the user with validation or additional logic."""
        if new_status not in ['request', 'valid', 'rejected']:
            raise ValueError("Invalid status")
        self.status = new_status
