#Handles all conection with SQL database for API keys
import sqlite3
from flask import g

DATABASE = "site.db"  # Change this if your DB file is different

def get_db():
    if "db" not in g:  # `g` is a special object that holds request data
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Close the database connection at the end of a request
def init_app(app):
    app.teardown_appcontext(close_db)
