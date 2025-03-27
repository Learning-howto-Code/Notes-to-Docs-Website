from flask import Blueprint, session, jsonify
import requests
from .db_utils import get_api_key

api_bp = Blueprint("api", __name__)

@api_bp.route("/use_api", methods=["GET"])
def use_api():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    api_key = get_api_key(session["user_id"])
    if not api_key:
        return jsonify({"error": "API key not found"}), 403

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://example.com/protected-resource", headers=headers)
    return jsonify(response.json())
