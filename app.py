"""
This module implements a Flask web application for managing children's rules 
and ratings. It allows users to display rules, assign star ratings to each child 
for different days, and store this information in an SQLite database.
"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DAYS_OF_WEEK = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

def connect_db():
    """Connect to the SQLite database and set the row factory."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Allow results to be accessed by column name
    return conn

def init_db():
    """Initialize the database and create tables if they do not exist."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS children (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )''')
        
    cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        child_id INTEGER,
                        rule_id INTEGER,
                        day TEXT,
                        stars INTEGER CHECK(stars >= 0 AND stars <= 2)
                    )''')
    
    cursor.execute("SELECT COUNT(*) FROM children")
    if cursor.fetchone()[0] == 0:
        children = [("Maya",), ("Ella",), ("Keziah",)]
        cursor.executemany("INSERT INTO children (name) VALUES (?)", children)
        
    conn.commit()
    conn.close()

@app.route("/")
def home():
    """Display the home page showing the results of ratings."""
    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve rules and children from the database
    cursor.execute("SELECT * FROM rules")
    rules = cursor.fetchall()

    cursor.execute("SELECT * FROM children")
    children = cursor.fetchall()

    ratings_dict = {}
    for child in children:
        for rule in rules:
            for day in DAYS_OF_WEEK:
                cursor.execute("SELECT stars FROM ratings WHERE child_id = ? AND rule_id = ? AND day = ?", 
                               (child["id"], rule["id"], day))
                rating = cursor.fetchone()
                stars = rating["stars"] if rating else 0
                ratings_dict[(child["id"], rule["id"], day)] = stars

    conn.close()
    return render_template("home.html", children=children, days=DAYS_OF_WEEK, rules=rules, ratings_dict=ratings_dict)

@app.route("/rate", methods=["GET"])
def rate():
    """Afficher les enfants, règles et jours avec possibilité de filtrer ou de sélectionner tout"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rules")
    rules = cursor.fetchall()

    cursor.execute("SELECT * FROM children")
    children = cursor.fetchall()

    selected_rule_id = request.args.get("rule_id")
    selected_rule = None

    if selected_rule_id != 'all' and selected_rule_id:
        cursor.execute("SELECT * FROM rules WHERE id = ?", (selected_rule_id,))
        selected_rule = cursor.fetchone()

    selected_day = None if request.args.get("day") == 'all' else request.args.get("day")

    ratings_dict = {}
    
    for child in children:
        for rule in (rules if not selected_rule else [selected_rule]):
            for day in (DAYS_OF_WEEK if not selected_day else [selected_day]):
                cursor.execute("SELECT stars FROM ratings WHERE child_id = ? AND rule_id = ? AND day = ?", 
                               (child["id"], rule["id"], day))
                rating = cursor.fetchone()
                ratings_dict[(child["id"], rule["id"], day)] = rating["stars"] if rating else 0
  
    conn.close()

    return render_template("rate.html", 
                           children=children, 
                           rules=rules, 
                           selected_rule=selected_rule, 
                           selected_day=selected_day, 
                           days_of_week=DAYS_OF_WEEK, 
                           ratings_dict=ratings_dict)
    
@app.route("/submit_rating", methods=["POST"])
def submit_rating():
    """Submit the rating for children based on the selected rule and day."""
    # Iterate over the submitted ratings
    for key in request.form:
        if key.startswith("stars_"):
            # Extract child_id, rule_id and day from the key
            parts = key.split('_')
            if len(parts) == 4:  # stars_<child_id>_<rule_id>_<day>
                child_id = parts[1]
                rule_id = parts[2]
                day = parts[3]
                stars = request.form[key]

                conn = connect_db()
                cursor = conn.cursor()

                # Check if a rating already exists for this child, rule, and day
                cursor.execute("SELECT * FROM ratings WHERE child_id = ? AND rule_id = ? AND day = ?", (child_id, rule_id, day))
                existing_rating = cursor.fetchone()

                if existing_rating:
                    # Update the existing rating
                    cursor.execute("UPDATE ratings SET stars = ? WHERE id = ?", (stars, existing_rating["id"]))
                else:
                    # Add a new rating
                    cursor.execute("INSERT INTO ratings (child_id, rule_id, day, stars) VALUES (?, ?, ?, ?)", 
                                   (child_id, rule_id, day, stars))

                conn.commit()
                conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()  # Initialize the database on startup
    app.run(debug=True)
