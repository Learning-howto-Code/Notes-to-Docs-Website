import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Define db globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass  # Handle potential OS errors
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        # Fix the path - remove redundant components
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'site.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Initialize the database with app
    db.init_app(app)
    
    # Import routes AFTER db is initialized
    from flask_test.routes import main
    app.register_blueprint(main)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
        
    return app