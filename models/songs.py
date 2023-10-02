from app import db

class MyPlayedTrack(db.Model):
    __tablename__ = 'played_tracks'
    song_name = db.Column(db.String(200))
    artist_name = db.Column(db.String(200))
    played_at = db.Column(db.String(200), primary_key=True, unique=True)
    timestamp = db.Column(db.String(200))
    spotifyid = db.Column(db.String(200), db.ForeignKey('Profile.spotifyid'))
    song_id = db.Column(db.String(200), primary_key=True)

    def __init__(self, song_name, artist_name, played_at, timestamp, spotifyid, song_id):
        self.song_name = song_name
        self.artist_name = artist_name
        self.played_at = played_at
        self.timestamp = timestamp
        self.spotifyid = spotifyid
        self.song_id = song_id