"""
Flask app that shows all users from https://jsonplaceholder.typicode.com/users

Run:
  pip install flask requests
  python app.py

Then open http://127.0.0.1:5000/
"""
from flask import Flask, render_template, abort
import requests

app = Flask(__name__, template_folder="templates")

USERS_API = "https://jsonplaceholder.typicode.com/users"

@app.route("/")
def show_users():
    """
    Fetch users from JSONPlaceholder and render the users.html template.
    Returns a 502 with a friendly message if the upstream request fails.
    """
    try:
        resp = requests.get(USERS_API, timeout=5)
        resp.raise_for_status()
        users = resp.json()
        # Ensure we have a list
        if not isinstance(users, list):
            return render_template("users.html", users=[], error="Unexpected API response format"), 502
        return render_template("users.html", users=users, error=None)
    except requests.RequestException as exc:
        # Return template with an error message and 502 status
        return render_template("users.html", users=[], error=str(exc)), 502

if __name__ == "__main__":
    # Development server
    app.run(host="127.0.0.1", port=5000, debug=True)
