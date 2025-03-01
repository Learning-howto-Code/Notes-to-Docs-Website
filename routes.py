from flask import render_template, request, jsonify, redirect, url_for, flash, Blueprint
from flask_test.models import db
from flask_test.models import User
from flask_login import login_user, login_required, logout_user, current_user
from flask_test.forms import LoginForm, RegistrationForm
import os
import shutil
import base64
import json
from openai import OpenAI
from pydantic import BaseModel
from flask_test.keys import OPENAI_KEY

main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return render_template('index.html')

# Registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, key=form.key.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Use password hashing!
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

# Dashboard route
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

# Index route (Duplicate of home, can be removed)
@main.route('/index')
def index():
    return render_template('index.html')

# Logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

# OpenAI conversion route
class Output(BaseModel):
    text: str

@main.route('/convert', methods=['POST'])
def convert():
    client = OpenAI(api_key=OPENAI_KEY)
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    folder = "/path/to/your/uploads"
    
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
