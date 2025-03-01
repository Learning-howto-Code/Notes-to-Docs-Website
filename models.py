from flask_test import db  # Import db from __init__, NOT the other way around

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    key = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'