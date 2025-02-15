from flask import Blueprint, request, jsonify, send_from_directory
import os

uploads_bp = Blueprint("uploads", __name__)  # Create a Blueprint

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

@uploads_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("file")  # Get multiple files
    uploaded_files = []
    
    for file in files:
        if file.filename:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            uploaded_files.append(file.filename)

    return jsonify({"message": "Files uploaded successfully!", "files": uploaded_files})

@uploads_bp.route("/files")
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files})

@uploads_bp.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
