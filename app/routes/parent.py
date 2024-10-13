""" app/routes/parent.py"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
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

    selected_child_id = request.args.get("child_id")
    selected_child = None

    if selected_child_id != 'all' and selected_child_id:
        selected_child = Child.query.filter_by(id=selected_child_id).first()


    selected_rule_id = request.args.get("rule_id")
    selected_rule = None

    if selected_rule_id != 'all' and selected_rule_id:
        selected_rule = Rule.query.filter_by(id=selected_rule_id).first()

    selected_day = None if request.args.get("day") == 'all' else request.args.get("day")

    ratings_dict = {}
    for child in (all_children if not selected_child else [selected_child]):
        for rule in (all_rules if not selected_rule else [selected_rule]):
            for day in (DAYS_OF_WEEK if not selected_day else [selected_day]):                            
                lrating = Rating.query.filter_by(
                    child_id=child.id,
                    rule_id=rule.id,
                    day=day
                ).first()

                # Mettre à jour le dictionnaire des notations
                ratings_dict[(child.id, rule.id, day)] = lrating.stars if lrating else 0

    return render_template("rating.html",
                           selected_child=selected_child,
                           selected_rule=selected_rule,
                           selected_day=selected_day,
                           children=all_children,
                           days_of_week=DAYS_OF_WEEK,
                           rules=all_rules,
                           ratings_dict=ratings_dict)

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

@parent_bp.route('/children/delete/<int:child_id>', methods=['POST'])
@role_required('parent')
def delete_child(child_id):
    """Retirer un enfant."""
    child = Child.query.get_or_404(child_id)
    db.session.delete(child)
    db.session.commit()
    flash("Enfant retirer de la liste avec avec succès.", "success")
    return redirect(url_for('parent.list_children'))


def get_paginated_rules(page, per_page=10):
    """get_paginated_rules"""
    return Rule.query.paginate(page=page, per_page=per_page, error_out=False)

@parent_bp.route('/rules', methods=['GET'])
@role_required('parent')
def manage_rules():
    """afficher et gérer les règles"""
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Nombre de règles par page

    paginated_rules = get_paginated_rules(page, per_page)


    return render_template('manage_rules.html', rules=paginated_rules.items, total=paginated_rules.total, page=page, per_page=per_page)

@parent_bp.route('/rules/add', methods=['POST'])
@role_required('parent')
def add_rule():
    """Ajouter une règle."""
    rule_name = request.form.get('new_rule')
    rule_description = request.form.get('rule_description')
    if rule_name and rule_description:
        new_rule = Rule(name=rule_name, description=rule_description)
        db.session.add(new_rule)
        db.session.commit()
        flash("Règle ajoutée avec succès.", "success")
    else:
        flash("Le nom et la description de la règle sont obligatoires.", "error")
    return redirect(url_for('parent.manage_rules'))

@parent_bp.route('/rules/edit/<int:rule_id>', methods=['POST'])
@role_required('parent')
def edit_rule(rule_id):
    """Editer une règle."""
    rule = Rule.query.get_or_404(rule_id)

    rule.name = request.form.get('rule_name')
    rule.description = request.form.get('rule_description')
    db.session.commit()
    flash("Règle mise à jour avec succès.", "success")
    return redirect(url_for('parent.manage_rules'))

@parent_bp.route('/rules/delete/<int:rule_id>', methods=['POST'])
@role_required('parent')
def delete_rule(rule_id):
    """Supprimer une règle."""
    rule = Rule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    flash("Règle supprimée avec succès.", "success")
    return redirect(url_for('parent.manage_rules'))
