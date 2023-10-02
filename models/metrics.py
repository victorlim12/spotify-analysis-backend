from app import db

class Metric(db.Model):
    __tablename__ = 'track_metrics'
    song_id = db.Column(db.String(200), primary_key=True,  unique=True)
    song_name = db.Column(db.String(200))
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    tempo = db.Column(db.Float)
    liveness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    acousticness = db.Column(db.Float)

    def __init__(self, song_id, song_name, danceability, energy, key, loudness, tempo, liveness, speechiness, acousticness):
        self.song_id = song_id
        self.song_name = song_name
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.tempo = tempo
        self.liveness = liveness
        self.speechiness = speechiness
        self.acousticness = acousticness