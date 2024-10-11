""" app/routes/__init__.py"""
from app.routes.main import main_bp
from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.parent import parent_bp

# Liste des blueprints disponibles dans l'application
__all__ = ['main_bp', 'admin_bp', 'auth_bp', 'parent_bp']
