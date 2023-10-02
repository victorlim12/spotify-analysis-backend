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
        metric_df=Extract.get_song_metrics(load_df, access_token)

        song_name = load_df['song_name'].tolist()
        artist_name = load_df['artist_name'].tolist()
        played_at = load_df['played_at'].tolist()
        timestamp = load_df['timestamp'].tolist()
        spotify_id = load_df['spotifyid'].tolist()
        song_id = load_df['song_id'].tolist()

        # Create instances of MyPlayedTrack and Metric using a loop
        for i in range(len(song_name)):
            print(i)
            song_history = MyPlayedTrack(
                song_name=song_name[i],
                artist_name=artist_name[i],
                played_at=played_at[i],
                timestamp=timestamp[i],
                spotifyid=spotify_id[i],
                song_id=song_id[i]
            )

            db.session.add(song_history)
            db.session.commit()

        return jsonify({"message": 'loading performed successfully', "code":200})
    except Exception as e:
        return jsonify({"message": f'loading failed, error: {e}', "code":500})