from app import db

class Profile(db.Model):
    __tablename__ = 'Profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Integer, db.ForeignKey('account.username'), unique=True, nullable=False)
    spotifyid = db.Column(db.String(255), unique=True)  # Assuming Spotify IDs are strings
    email = db.Column(db.String(255), unique=True)

    def __init__(self, username, spotifyid, email ):
        self.username = username
        self.spotifyid = spotifyid
        self.email = email