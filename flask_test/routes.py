from flask import render_template, request, jsonify, redirect, url_for, flash, Blueprint, session, flash
from flask_test import db
from flask_test.models import User
from flask_login import login_user, login_required, logout_user, current_user
from flask_test.forms import LoginForm, RegistrationForm
import os
import shutil
import base64
import json
from openai import OpenAI
from pydantic import BaseModel
# from flask_test.keys import OPENAI_KEY

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
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
         flash("Email address already registered. Please use a different email.", "danger")
         return redirect(url_for('main.register'))
    
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
def logout():
    if not current_user.is_authenticated:
        flash('You are not logged in.', 'warning')
    else:
        logout_user()
        flash('You have been logged out.', 'warning')
    return redirect(url_for('main.home'))

@main.route('/delete')
@login_required
def delete():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    flash('your acount has been deleted', 'succes')
    return redirect(url_for('main.home'))

# Dashboard route
@main.route('/settings')
def settings():
    if not current_user.is_authenticated:
        flash('Must be logged in to view setings', 'danger')
        return redirect(url_for('main.home'))
    return render_template('settings.html', message='test message')

@main.route('/protected-action')
def protected_action():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return "You accessed a protected action!"

def button_press():
    # Ensure user is logged in
    if not session.get('user_logged_in'):  # Check if user is logged in
        flash('You must be logged in to upload files.', 'warning')  # Flash the warning
    return render_template('home.html')


