""" app/routes/parent.py"""
from flask import Blueprint, render_template, request
from app.utils.decorators import login_required, role_required
from app.models import Rule, Child, Rating

# Création du Blueprint pour les routes des actions parent
parent_bp = Blueprint('parent', __name__, url_prefix='/parent')


DAYS_OF_WEEK = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

@parent_bp.route('/rate', methods=['GET'])
@login_required
@role_required('parent')
def rate():
    """Afficher les enfants, règles et jours avec possibilité de filtrer ou de sélectionner tout"""

    # Retrieve all rules from the database
    all_rules = Rule.query.all()

    # Retrieve all children from the database
    all_children = Child.query.all()

    selected_rule_id = request.args.get("rule_id")
    selected_rule = None

    if selected_rule_id != 'all' and selected_rule_id:
        selected_rule = Rule.query.filter_by(id=selected_rule_id).first()

    selected_day = None if request.args.get("day") == 'all' else request.args.get("day")

    ratings_dict = {}
    for child in all_children:
        for rule in (all_rules if not selected_rule else [selected_rule]):
            for day in (DAYS_OF_WEEK if not selected_day else [selected_day]):
                # Récupérer la notation correspondant en utilisant SQLAlchemy
                rating = Rating.query.filter_by(
                    child_id=child.id,
                    rule_id=rule.id,
                    day=day
                ).first()

                # Mettre à jour le dictionnaire des notations
                ratings_dict[(child.id, rule.id, day)] = rating.stars if rating else 0

    return render_template("rating.html", children=all_children,
                           days=DAYS_OF_WEEK, rules=all_rules, ratings_dict=ratings_dict)
