""" app/routes/admin_bp.py"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User

# Création du Blueprint pour les routes d'administration
admin_db = Blueprint('admin', __name__, url_prefix='/admin')

@admin_db.route('/validate_users', methods=['GET', 'POST'])
def validate_users():
    """__summary__"""
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
        
        flash(f"Le statut de l'utilisateur {user.username} a été mis à jour.")
        return redirect(url_for('admin_bp.validate_users'))

    # Récupérer tous les utilisateurs en attente de validation
    user_in_request = User.query.filter_by(status='request').all()
    
    return render_template('validate_users.html', users=user_in_request)
