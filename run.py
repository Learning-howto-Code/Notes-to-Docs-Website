from flask_test import create_app, db

# Create the app instance
app = create_app()

# Create all the tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
