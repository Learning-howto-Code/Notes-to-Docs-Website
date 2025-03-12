from flask_test import db  # Import db from __init__.py after it's initialized
from flask_test.__init__ import db # Import db from __init__.py after it's initialized
from flask_test import db  # Import db from __init__.py after it's initialized
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    key = db.Column(db.String(50), unique=True, nullable=False)

    def get_id(self):
        return str(self.id)  # Required by Flask-Login
    def get_id(self):
        return str(self.id)  # Required by Flask-Login
    def get_id(self):
        return str(self.id)  # Required by Flask-Login

