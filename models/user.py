from app import db

class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Add other user attributes as needed

    def __init__(self, username, password):
        self.username = username
        self.password = password
