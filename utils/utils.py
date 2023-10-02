import jwt
import os
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps
from datetime import datetime, timedelta
import requests

JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')

def generate_token(payload):
    token = jwt.encode(payload,JWT_SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
# require jwt to wrap
def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT in the request
            verify_jwt_in_request()
            # If JWT is valid, call the protected route
            return fn(*args, **kwargs)
        except Exception as e:
            return {'error': 'JWT authentication required'}, 401
    return wrapper

def refresh_access_token(token_record):
    from app import db
    current_time = datetime.now()

    if token_record.token_expiration and current_time < token_record.token_expiration:
        # Token is still valid, no need to refresh
        return token_record.access_token
    

    # Token has expired, refresh it using the refresh token
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token_record.refresh_token,
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        new_access_token = token_data.get('access_token')
        new_token_expiration = current_time + timedelta(seconds=token_data.get('expires_in'))

        # Update the access token and token expiration in the database
        token_record.access_token = new_access_token
        token_record.token_expiration = new_token_expiration
        token_record.last_refreshed = current_time
        db.session.commit()

        return new_access_token
    else:
        # Handle token refresh failure here, such as logging the error or taking appropriate actions
        return None