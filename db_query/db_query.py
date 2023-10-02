from flask import session, Blueprint, request, jsonify, redirect
import requests
import os
import uuid
import urllib
import webbrowser
from dotenv import load_dotenv
import jwt
import json
import pandas as pd

from utils.utils import jwt_required_custom
from db_query.analytics import *
from flask_jwt_extended import create_access_token, get_jwt_identity

db_query = Blueprint('db_query', __name__)
JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')

@db_query.route('/getAnalytics')
@jwt_required_custom
def get_user():
    from app import db
    from models.profile import Profile
    from models.songs import MyPlayedTrack
    try:
        token_client = get_jwt_identity()
        username = token_client.get('username')
        user_profile = db.session.query(Profile).filter(Profile.username == username).first()

        if user_profile:
            # Assuming you have a foreign key relationship between Profile and MyPlayedTrack
            song_history = db.session.query(MyPlayedTrack).join(Profile).filter(Profile.username == username).all()
            song_history_data = []
            for track in song_history:
                song_history_data.append({
                    'song_name': track.song_name,
                    'artist_name': track.artist_name,
                    'played_at': track.played_at,
                    'timestamp': track.timestamp,
                    'spotifyid': track.spotifyid,
                    'song_id': track.song_id
                })

            # Create a Pandas DataFrame
            song_history_df = pd.DataFrame(song_history_data)
            top_songs_dict, unique_songs,listening_hours_dict, top_hours= listening_analytics(song_history_df)

            # Construct the analytics data response
            analytics_data = {
                'topSongs': top_songs_dict,
                'uniqueSongs':unique_songs,
                'listeningPattern': listening_hours_dict,
                'topHours': top_hours
                # Add more analytics here based on your needs
            }
            return jsonify(analytics_data), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


