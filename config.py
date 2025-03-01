import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key'  # Use os.environ.get('SECRET_KEY') in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')  # Change to MySQL or PostgreSQL if needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False
