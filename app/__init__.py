"""init"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import DevelopmentConfig, ProductionConfig

#Initialisation des extensiosn
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
load_dotenv()

# Import User model (you would replace 'app.models' with your actual module)
from app.models.user import User # pylint: disable=C0413

# Define the user_loader callback
@login_manager.user_loader
def load_user(user_id):
    """user_loader callback"""
    return User.query.get(int(user_id))

def create_app():
    """Create an instance of the Flask app"""
    app = Flask(__name__)

    # Load configuration
    config_class = DevelopmentConfig if os.environ.get('FLASK_ENV') == 'development' else ProductionConfig
    app.config.from_object(config_class)

    # Initialize the database with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    #Configurer la gestion des sessions utilisateurs
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'info'

    #Importer et enregistrer les blueprints
    # lazy import dans le but d'éviter des dépendances circulaires
    from app.routes.auth import auth_bp # pylint: disable=C0415
    from app.routes.main import main_bp # pylint: disable=C0415
    from app.routes.admin import admin_bp # pylint: disable=C0415
    from app.routes.parent import parent_bp # pylint: disable=C0415

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(parent_bp)

     # Créer les rôles par défaut et administrateur si non présents
    with app.app_context():
        from app.models.role import init_roles # pylint: disable=C0415
        from app.init_db import create_admin # pylint: disable=C0415

        db.create_all()

        init_roles()  # Appel pour créer les rôles
        create_admin()  # Appel pour créer un administrateur

    return app
