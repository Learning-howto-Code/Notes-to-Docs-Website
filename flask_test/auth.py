from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from .db_utils import get_db  # Your function to access the database

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.json  # Assuming you're sending JSON
    username = data.get("username")
    password = data.get("password")
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["api_key"] = user["key"]  # Save the user's API key in the session
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
