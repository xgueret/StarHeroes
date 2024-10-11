"""app/init_db.py"""
import os
from dotenv import load_dotenv
from app.models.user import User
from app import db

load_dotenv()

def create_admin():
    """creation d'un administrateur"""
    if not User.query.filter_by(username=os.environ.get('DEFAULT_ADMIN_NAME')).first():
        admin = User(username=os.environ.get('DEFAULT_ADMIN_NAME'),
                     email=os.environ.get('DEFAULT_ADMIN_EMAIL'))
        admin.set_password(os.environ.get('DEFAULT_ADMIN_PASSWORD') )
        admin.add_role('admin')
        admin.set_status('valid')
        db.session.add(admin)
        db.session.commit()
