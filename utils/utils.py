import jwt
import os
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps

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