import jwt
import os

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