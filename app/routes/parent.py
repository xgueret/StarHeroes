""" app/routes/parent.py"""
from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.utils.decorators import role_required
from app.models import Rule, Child, Rating

# Création du Blueprint pour les routes des actions parent
parent_bp = Blueprint('parent', __name__, url_prefix='/parent')


DAYS_OF_WEEK = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

@parent_bp.route('/rating', methods=['GET'])
@role_required('parent')
def rating():
    """Afficher les enfants, règles et jours avec possibilité de filtrer ou de sélectionner tout"""
    print("Afficher les enfants, règles et jours avec possibilité de filtrer ou de sélectionner tout")
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
                lrating = Rating.query.filter_by(
                    child_id=child.id,
                    rule_id=rule.id,
                    day=day
                ).first()

                # Mettre à jour le dictionnaire des notations
                ratings_dict[(child.id, rule.id, day)] = lrating.stars if lrating else 0

    return render_template("rating.html", children=all_children,
                           days=DAYS_OF_WEEK, rules=all_rules, ratings_dict=ratings_dict)

@parent_bp.route('/submit_rating', methods=['POST'])
@role_required('parent')
def submit_rating():
    """Submit the rating for children based on the selected rule and day."""
    for key in request.form:
        if key.startswith("stars_"):
            # Extract child_id, rule_id and day from the key
            parts = key.split('_')
            if len(parts) == 4:  # stars_<child_id>_<rule_id>_<day>
                child_id = parts[1]
                rule_id = parts[2]
                day = parts[3]
                stars = request.form[key]

                existing_rating = Rating.query.filter_by(child_id=child_id, rule_id=rule_id, day=day).first()

                if existing_rating:
                    # Update the existing rating
                    existing_rating.stars = stars
                else:
                    # Add a new rating
                    new_rating = Rating(child_id=child_id, rule_id=rule_id, day=day, stars=stars)
                    db.session.add(new_rating)

                db.session.commit()

    return redirect(url_for("main.home"))

@parent_bp.route('/children')
@role_required('parent')
def list_children():
    """Lister les enfants."""
    children = Child.query.all()
    return render_template('list_children.html', children=children)

@parent_bp.route('/children/add', methods=['POST'])
@role_required('parent')
def add_child():
    """Ajouter des enfants."""
    name = request.form['name']
    new_child = Child(name=name)
    db.session.add(new_child)
    db.session.commit()
    return redirect(url_for('parent.list_children'))
