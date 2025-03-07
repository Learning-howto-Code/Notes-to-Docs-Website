from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

uploads_bp = Blueprint("uploads", __name__)  # Blueprint name should match

UPLOAD_FOLDER = os.path.join(os.getcwd(), "/Users/jakehopkins/Documents/Flask_Test/uploads")  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

@uploads_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
         return "", 204  # No content response (silent)
    files = request.files.getlist("file")
    uploaded_files = []
    
    for file in files:
        if file.filename:
            safe_filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
            file.save(file_path)
            uploaded_files.append(safe_filename)
    
    if not uploaded_files:
        return jsonify({"error": "No files uploaded"}), 400
    
    return "", 204

@uploads_bp.route("/files", methods=["GET"])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": f"Error listing files: {str(e)}"}), 500

@uploads_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Error downloading file: {str(e)}"}), 404
