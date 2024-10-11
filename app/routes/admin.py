""" app/routes/admin.py"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models import User
from app.utils.decorators import login_required, role_required

# Création du Blueprint pour les routes d'administration
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/validate_users', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def validate_users():
    """Affiche la page pour la validation des instructeurs/trices."""
    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']

        # Trouver l'utilisateur dans la base de données
        user = User.query.get(user_id)

        if action == 'validate':
            user.status = 'valid'
        elif action == 'reject':
            user.status = 'rejected'

        db.session.commit()

        flash(f"Le statut de l'instructeur {user.username} a été mis à jour.")
        return redirect(url_for('admin_bp.validate_users'))

    # Récupérer tous les utilisateurs en attente de validation
    user_in_request = User.query.filter_by(status='request').all()

    return render_template('validate_users.html', users=user_in_request)
