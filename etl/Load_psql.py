from etl import Extract, Transform
import sqlalchemy
import pandas as pd 
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from flask import jsonify

def Load_PSQL(access_token, spotifyid):
    from models.songs import MyPlayedTrack
    from models.metrics import Metric
    from app import db
    try:
        #Importing the songs_df from the Extract.py
        load_df=Extract.get_listen_history(access_token, spotifyid)

        if(Transform.Data_Quality(load_df) == False):
            raise ("Failed at Data Validation")
        
        # Create instances of MyPlayedTrack and Metric using a loop
        for index,row in load_df.iterrows():
            song_history = MyPlayedTrack(
                song_name=row['song_name'],
                artist_name=row['artist_name'],
                played_at=row['played_at'],
                timestamp=row['timestamp'],
                spotifyid=row['spotifyid'],
                song_id=row['song_id']
            )

            db.session.merge(song_history)
        db.session.commit()

        metric_df=Extract.get_song_metrics(load_df, access_token)
        for index, row in metric_df.iterrows():
            song_metrics = Metric(
                song_id=row['song_name'],
                song_name=row['song_name'],
                danceability=row['danceability'],
                energy=row['energy'],
                key=row['key'],
                loudness=row['loudness'],
                tempo=row['tempo'],
                liveness=row['liveness'],
                speechiness=row['speechiness'],
                acousticness=row['acousticness'],
            )

            # Use merge() to perform upsert based on song_id
            db.session.merge(song_metrics)

        db.session.commit()

        return jsonify({"message": 'loading performed successfully', "code":200})
    except Exception as e:
        return jsonify({"message": f'loading failed, error: {e}', "code":500})