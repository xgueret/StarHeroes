"""
This module implements a Flask web application for managing children's rules 
and ratings. It allows users to display rules, assign star ratings to each child 
for different days, and store this information in an SQLite database.
"""
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def connect_db():
    """Connect to the SQLite database and set the row factory."""
    conn = sqlite3.connect('database.db')  # Connect to your SQLite database
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
        
    # Create the rules table if it does not already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule TEXT
                    )''')

    # Create the ratings table to store stars assigned to children
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        child_id INTEGER,
                        rule_id INTEGER,
                        day TEXT,
                        stars INTEGER CHECK(stars >= 0 AND stars <= 2)  -- Limit to 2 stars
                    )''')
    
    # Insert example children if the table is empty
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

    # Retrieve rules from the database
    cursor.execute("SELECT * FROM rules")
    rules = cursor.fetchall()

    cursor.execute("SELECT * FROM children")
    children = cursor.fetchall()
    
    # Prepare a dictionary to store ratings by (child_id, rule_id, day)
    ratings_dict = {}
    for child in children:
        for rule in rules:
            for day in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]:
                # Fetch ratings for the child, rule, and day
                cursor.execute("SELECT stars FROM ratings WHERE child_id = ? AND rule_id = ? AND day = ?", 
                               (child["id"], rule["id"], day))
                rating = cursor.fetchone()
                # Store the stars or default to 0
                stars = rating["stars"] if rating else 0
                ratings_dict[(child["id"], rule["id"], day)] = stars

    conn.close()

    # List of days of the week
    days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    return render_template("home.html", children=children, days=days_of_week, rules=rules, ratings_dict=ratings_dict)

@app.route("/rate")
def rate():
    """Display the rating page to assign stars to children."""
    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve rules from the database
    cursor.execute("SELECT * FROM rules")
    rules = cursor.fetchall()

    cursor.execute("SELECT * FROM children")
    children = cursor.fetchall()
    
    conn.close()

    return render_template("rate.html", children=children, rules=rules)

@app.route("/submit_rating", methods=["POST"])
def submit_rating():
    """Submit the rating for a child based on the selected rule and day."""
    child_id = request.form["child_id"]
    rule_id = request.form["rule_id"]
    day = request.form["day"]
    stars = request.form["stars"]

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
