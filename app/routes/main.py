"""__summary__"""
from flask import Blueprint, render_template, redirect, url_for, session
from app.models import User, Child, Rule, Rating
from app import db
from app.routes.auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Affiche la page d'accueil avec les règles et les notations des enfants."""
    rules = Rule.query.all()
    children = Child.query.all()
    
    #Obtenir les notations sous forme de dictionnaire
    ratings = Rating.query.all()
    ratings_dict = {(rating.child_id, rating.rule_id, rating.day): rating.stars for rating in ratings}
    
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    
    return render_template('home.html', rules=rules, children=children, ratings_dict=ratings_dict, days=days)

@main_bp.route('/validate_users')
@login_required
def validate_users():
    """Affiche la page pour la validation des utilisateurs."""
    return render_template('validate_users.html')
