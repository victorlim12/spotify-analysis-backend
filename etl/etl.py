from flask import session, Blueprint, request, jsonify, redirect
import requests
import os
import uuid
import urllib
import webbrowser
from dotenv import load_dotenv
import jwt
import json
import secrets

from utils.utils import *
from utils.utils import jwt_required_custom
from flask_jwt_extended import create_access_token, get_jwt_identity
from etl.Load_psql import Load_PSQL

##Define blueprint to be registered in the main app
##AUTH route is mainly for spotify interfacing for oAuthV2 --> first interfacing with react client 
etl = Blueprint('etl', __name__)

#get data from config
PORT= os.getenv("FLASK_PORT")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = f"http://localhost:{PORT}/auth/callback"
SPOTIFY_SCOPES = 'user-read-email user-read-private user-top-read user-read-recently-played'  # Add other scopes if needed
json_file_path ='access_token.json'

#define function for each auth purpose
@etl.route('/', methods=['POST'])
@jwt_required_custom
def run_etl():
    from models.user import Account 
    from models.token import Token  
    from models.profile import Profile

    from app import db
    try:
        token_client = get_jwt_identity()
        token = db.session.query(Token).filter_by(username=token_client.get('username')).first()        
        profile = db.session.query(Profile).filter_by(username=token_client.get('username')).first()
        access_token = refresh_access_token(token)
        response = Load_PSQL(access_token, profile.spotifyid)
        if response.json["code"]==200:
             return jsonify({'message': 'ETL completed, time to go query', 'code': 200})
        else:
            return jsonify({'message': f'ETL failed, error: {response.json["message"]}', 'code': 500})
    except Exception as e:
        return jsonify({'message': f'error found: {e}', 'code': 404})
    





