"""liste de décorateur"""
from functools import wraps
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_required

def role_required(role_name):
    """Décorateur pour exiger qu'un utilisateur ait un certain rôle."""
    def wrapper(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                if current_user.has_role(role_name):
                    return f(*args, **kwargs)
                else:
                    flash("Vous n'avez pas la permission d'accéder à cette page.", "danger")
                    return redirect(url_for('main.home'))
            else:
                return redirect(url_for('auth.login', next=request.url))
        return decorated_function
    return wrapper
