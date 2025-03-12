from .database import get_db  # Assuming you have a function to get your DB connection

def get_api_key(user_id):
    db = get_db()
    user = db.execute("SELECT key FROM users WHERE id = ?", (user_id,)).fetchone()
    return user["key"] if user else None
