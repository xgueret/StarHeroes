""" app/routes/auth.py"""
from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User

# Création du Blueprint pour les routes d'authentification
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# la route pour afficher la page de connexion
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Affiche le formulaire d'authentification des utilisateurs"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

         # chercher l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()

        # Vérifier si l'utilisateur existe déjà et si le mot de passe est correct
        if user is None or not user.check_password(password):
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
            return redirect(url_for('auth.login'))

        # Vérifier le statut de l'utilisateur
        if user.status == 'request':
            flash('Votre demande d\'inscription est en attente de validation.', 'warning')
            return redirect(url_for('auth.login'))
        elif user.status == 'rejected':
            flash('Votre demande d\'inscription a été rejetée', 'error')
            return redirect(url_for('auth.login'))

        # Si l'utilisateur est validé, il peut se connecter
        #session['user_id'] = user.id
        login_user(user)
        #flash('Connexion réussie', 'success')
        return redirect(url_for('main.home')) # Rediriger vers la page d'accueil

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Route pour déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté!', 'success')
    return redirect(url_for('auth.login'))

# Route pour afficher la page d'inscription
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Affiche le formulaire d'inscription"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        role     = request.form['role']

        # Vérifier si l'utilisateur existe déjà
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Nom d\'utilisateur déjà pris', 'warning')
            return redirect(url_for('auth.register'))

        # Créer un nouvel utilisateur avec le statut 'request'
        new_user = User(username=username, email=email, status='request')
        new_user.set_password(password)
        new_user.add_role(role)

        db.session.add(new_user)
        db.session.commit()

        flash('Votre demande d\'inscription a été envoyée. Un administrateur doit la valider', 'warning')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
