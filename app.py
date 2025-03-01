from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import shutil
import base64
import json
from openai import OpenAI
from pydantic import BaseModel
from googleapiclient.discovery import build
from google.oauth2 import service_account
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from uploads import uploads_bp
from keys import OPENAI_KEY
from routes import app # Import routes but leave models import for later
from flask_test import app
from flask_test.forms import LoginForm, RegistrationForm
from flask_migrate import Migrate

# Add Flask-Migrate import
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(uploads_bp, url_prefix="/uploads")

# Configure app
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Now import User AFTER db and login_manager are defined
from .models import User  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Your model output schema
class Output(BaseModel):
    text: str

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def convert():
    client = OpenAI(api_key=OPENAI_KEY)
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    folder = "/Users/jakehopkins/Documents/Flask_Test/uploads"
    
    if not os.path.exists(folder):
        return jsonify({"message": "Folder not found!"}), 400
    
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        return jsonify({"message": "No image files found!"}), 400
    
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
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=2000,
            timeout=60
        )
        
        json_output = response.choices[0].message.content
        structured_output = Output.model_validate(json.loads(json_output))
        results.append({image_file: structured_output.model_dump()})
        
        print("Conversion Results:")
        print(results)
    
    return jsonify({"message": "Conversion successful!", "results": results})

def append_to_docs():
    SERVICE_ACCOUNT_FILE = "/Users/jakehopkins/Documents/Flask_Test/img-to-docs-450117-078405c7be8a copy.json"
    SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    docs_service = build("docs", "v1", credentials=credentials)
    drive_service = build("drive", "v3", credentials=credentials)

    document_id = "1Nq9OTr-sQrkNvkGD3LjTJzjfrWv6XUmSL8Ycx1Ko4JU"

    USER_EMAIL = "jaketoroh@gmail.com"  # Replace with your email

    def add_text(text):
        """Adds text to the Google Doc."""
        requests = [
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": text + "\n"
                }
            }
        ]
        
        docs_service.documents().batchUpdate(
            documentId=document_id,  # Fix: Use the correct document ID
            body={"requests": requests}
        ).execute()

# Ensure database tables are created before running
with app.app_context():
    db.create_all()

# Initialize migrations for Flask-Migrate
if __name__ == "__main__":
    app.run(debug=True)
