from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .uploads import uploads_bp

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)

    # Move the import here to avoid circular import
    from flask_test.models import User  
    from flask_test.routes import main  
    app.register_blueprint(main)
    app.register_blueprint(uploads_bp, url_prefix="/uploads")

    return app

@login_manager.user_loader
def load_user(user_id):
    from flask_test.models import User  # Import inside function to avoid circular import
    return User.query.get(int(user_id))
