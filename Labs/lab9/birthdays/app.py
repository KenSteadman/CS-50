import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the user's input from the form
        alert_message = ""
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        if not name:
            alert_message = "Missing name"
        elif not month:
            alert_message = "Missing month"
        elif not day:
            alert_message = "Missing day"
        else:

            # Insert the new birthday into the database
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        # Redirect to the index page to display the updated list of birthdays
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", message=alert_message, birthdays=birthdays)

    else:
        # Query the database for all birthdays
        birthdays = db.execute("SELECT * FROM birthdays")

        # Render the template with the list of birthdays
        return render_template("index.html", birthdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():
    # Get the id of the row to be deleted from the form
    id = request.form.get("id")

    if id:
        # Delete the row from the database
        db.execute("DELETE FROM birthdays WHERE id = ?", id)

    # Redirect to the index page to display the updated list of birthdays
    return redirect("/")
