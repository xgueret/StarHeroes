""" app/routes/auth_bp.py"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app import db
from app.models import User

# Création du Blueprint pour les routes d'authentification
auth_db = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    """Décorateur pour exiger qu'un utilisateur soit connecté pour accéder à certaines routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: # vérifie si l'utilisateur est connecté
            return redirect(url_for('auth.login', next=request.url)) # redirige vers la page de connexion
        return f(*args, **kwargs)
    return decorated_function

# la route pour afficher la page de connexion
@auth_db.route('/login', methods=['GET', 'POST'])
def login():
    """_summary_"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # chercher l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()
        
        # Vérifier si l'utilisateur existe déjà et si le mot de passe est correct
        if user is None or not user.check_password(password):
            flash('Bom d\'utilisateur our mot de passe incorrect.')
            return redirect(url_for('auth_bp.login'))
        
        # Vérifier le statut de l'utilisateur
        if user.status == 'request':
            flash('Votre demande d\'inscription est en attente de validation.')
            return redirect(url_for('auth_bp.login'))
        elif user.status == 'rejected':
            flash('Votre demande d\'inscription a été rejetée')
            return redirect(url_for('auth_bp.login'))
        
        # Si l'utilisateur est validé, il peut se connecter
        session['user_id'] = user.id
        return redirect(url_for('home')) # Rediriger vers la page d'accueil
        
    return render_template('auth/login.html')

# Route pour afficher la page d'inscription
@auth_db.route('/register')
def register():
    """__summary__"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier si l'utilisateur existe déjà
        user_exists = User.query.filter_by(username).first()
        if user_exists: 
            flash('Nom d\'utilisateur déjà pris')
            return redirect(url_for('auth_db.register'))
        
        # Créer un nouvel utilisateur avec le statut 'request'
        new_user = User(username=username, status='request')
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Votre demande d\'inscription a été envoyée. Un administrateur doit la valider')
        return redirect(url_for('auth_bp.login'))
    
    return render_template('register.html')
