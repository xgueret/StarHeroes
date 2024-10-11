"""liste de décorateur"""
from functools import wraps
from flask import session, redirect, url_for, request, flash
from app.models.user import User

def login_required(f):
    """Décorateur pour exiger qu'un utilisateur soit connecté pour accéder à certaines routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: # vérifie si l'utilisateur est connecté
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role_name):
    """Décorateur pour exiger qu'un utilisateur ait un certain rôle."""
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                if user and user.has_role(role_name):
                    return f(*args, **kwargs)
            flash("Vous n'avez pas la permission d'accéder à cette page.", "danger")
            return redirect(url_for('auth.login'))
        return decorated_function
    return wrapper
