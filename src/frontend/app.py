"""Runs the front end application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Serve main page"""
    return render_template("index.html")


@app.route("/character")
def character():
    """Serve character page"""
    return render_template("character.html")


if __name__ == "__main__":
    app.run(debug=True)
