"""init"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import DevelopmentConfig, ProductionConfig

# Charger les variables d'environnement
load_dotenv()

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

# Importer le modèle User
from app.models.user import User  # pylint: disable=C0413

# Définir la fonction de rappel pour le chargement des utilisateurs
@login_manager.user_loader
def load_user(user_id):
    """Callback pour charger un utilisateur à partir de son identifiant"""
    return User.query.get(int(user_id))

def create_app():
    """Créer une instance de l'application Flask"""
    app = Flask(__name__)

    # Charger la configuration en fonction de l'environnement
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Initialiser les extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Configurer la gestion des sessions utilisateurs
    login_manager.login_view = 'auth.login'  # Vue de connexion par défaut
    login_manager.login_message_category = 'info'  # Catégorie des messages de connexion

    # Importer et enregistrer les blueprints
    # Lazy imports pour éviter les dépendances circulaires
    from app.routes.auth import auth_bp  # pylint: disable=C0415
    from app.routes.main import main_bp  # pylint: disable=C0415
    from app.routes.admin import admin_bp  # pylint: disable=C0415
    from app.routes.parent import parent_bp  # pylint: disable=C0415

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(parent_bp)

    # Créer les rôles par défaut et un administrateur si non présents
    with app.app_context():
        from app.models.role import init_roles  # pylint: disable=C0415
        from app.init_db import create_admin  # pylint: disable=C0415

        db.create_all()  # Créer les tables si elles n'existent pas encore

        init_roles()  # Créer les rôles par défaut
        create_admin()  # Créer un utilisateur administrateur par défaut

    return app
