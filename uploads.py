from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
# from .keys import OPENAI_KEY
import base64
from openai import OpenAI
from pydantic import BaseModel
import json
from .docs_api import add_text
from flask_login import current_user, login_required

uploads_bp = Blueprint("uploads", __name__)  # Blueprint name should match

UPLOAD_FOLDER = os.path.join(os.getcwd(), "/Users/jakehopkins/Documents/Flask_Test/uploads")  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
@login_required
@uploads_bp.route("/upload", methods=["POST"])
def upload_file():
    # Clear the uploads directory before saving new files
    for file_name in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file
        except Exception as e:
            return jsonify({"error": f"Failed to clear directory: {str(e)}"}), 500

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

    # Call convert() after images are uploaded
    convert_result = convert()  # This runs the OCR process

    return jsonify({
        "message": "Files uploaded successfully!",
        "conversion_result": convert_result  # Pass the response from convert()
    })

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
def convert():
    client = OpenAI(api_key=current_user.key)# uses the logged in key instead of hard coded key

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    folder = UPLOAD_FOLDER  # Use the same uploads folder

    if not os.path.exists(folder):
        return {"message": "Folder not found!"}

    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        return {"message": "No image files found!"}

    results = []

    for image_file in image_files:
        image_path = os.path.join(folder, image_file)
        base64_image = encode_image(image_path)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract the text from this image word for word and return it in JSON format with a 'text' field containing the extracted text as a string."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}",
                                        "detail": "low"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=2000,
            timeout=60
        )

        json_output = response.choices[0].message.content
        structured_output = json.loads(json_output)  # Parse JSON response
        results.append({image_file: structured_output})

    # Extract the text from results and join it into a single string
    text_to_add = "\n".join([item[list(item.keys())[0]]['text'] for item in results])

    # Call the add_text function to add the extracted text to Google Docs
    add_text(text_to_add)
    print(text_to_add)

    return {"message": "Conversion successful!", "results": results}
