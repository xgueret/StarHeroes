""" app/routes/__init__.py"""
from app.routes.auth_bp import auth_db


# Liste des blueprints disponibles dans l'application
__all__ = ['auth_db']
