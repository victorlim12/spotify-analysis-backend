from app import db
import hashlib
import os

class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    authorized = db.Column(db.Boolean, default=False)

    # Add other user attributes as needed

    def __init__(self, username, password, authorized=False):
        self.username = username
        self.salt = os.urandom(32).hex()  # Generate a random salt
        self.password_hash = self._hash_password(password)
        self.authorized = authorized
    
    def _hash_password(self, password):
        # Hash the password using a salt
        salted_password = password + self.salt
        return hashlib.sha256(salted_password.encode()).hexdigest()
    
    def check_password(self, password):
        # Hash the provided password with the stored salt and compare it to the stored password_hash.
        salted_password = password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed_password == self.password_hash
