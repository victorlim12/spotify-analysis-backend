from app import db
from datetime import datetime

class Token(db.Model):
    __tablename__ = 'Token'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Account.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    token_expiration = db.Column(db.DateTime)  # Token expiration timestamp
    last_refreshed = db.Column(db.DateTime, default=datetime.now())  # Timestamp when token was last refreshed
    
    def __init__(self, access_token, refresh_token, user_id, username, token_expiration):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.username = username
        self.token_expiration = token_expiration