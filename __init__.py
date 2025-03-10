from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .db import init_app  # Import your database setup function

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    init_app(app)  # Initialize SQLite database

    from .auth import auth_bp
    from .routes import main
    from .uploads import uploads_bp
    from .api import api_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main)
    app.register_blueprint(uploads_bp, url_prefix="/uploads")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
