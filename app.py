""" Description todo """
from flask import Flask, render_template

app = Flask(__name__)

# Liste des enfants
children = [
    {"name": "child1", "id": 1},
    {"name": "child2", "id": 2},
    {"name": "child3", "id": 3}
]

# Route principal pour afficher l'interface utilisateur
@app.route("/")
def home():
    """ Descriptio todo """
    days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    return render_template("home.html", children=children, days=days_of_week)

if __name__ == "__main__":
    app.run(debug=True)
