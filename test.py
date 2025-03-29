from flask_test import create_app
from flask import url_for

app = create_app()
app.testing = True

with app.test_client() as client:
    # Simulate login by posting to your login endpoint:
    login_response = client.post('/auth/login', json={
        "username": "your_username",
        "password": "your_password"
    })
    # Now that a user is logged in, access a protected route
    response = client.get('/test_user_key')  # A route that returns current_user.key
    print(response.get_data(as_text=True))
