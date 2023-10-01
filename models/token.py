from app import db

class Token(db.Model):
    __tablename__ = 'Token'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Account.id'), nullable=False)
    
    def __init__(self, access_token, refresh_token, user_id):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
