""" app/routes/main.py"""
from flask import Blueprint, render_template
from app.models import Rule, Child, Rating


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Affiche la page d'accueil avec les règles et les notations des enfants."""
    rules = Rule.query.all()
    children = Child.query.all()

    #Obtenir les notations sous forme de dictionnaire
    ratings = Rating.query.all()
    ratings_dict = {(rating.child_id,
                     rating.rule_id, rating.day): rating.stars for rating in ratings}

    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

    return render_template('home.html', rules=rules,
                           children=children, ratings_dict=ratings_dict, days=days)
