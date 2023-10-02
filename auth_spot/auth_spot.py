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
from datetime import datetime

##import utils for decode
from utils.utils import *
from models.user import Account 
from models.token import Token  
from models.profile import Profile
from models.songs import MyPlayedTrack
from models.metrics import Metric

from app import db
from utils.utils import jwt_required_custom
from flask_jwt_extended import create_access_token, get_jwt_identity

##Define blueprint to be registered in the main app
##AUTH route is mainly for spotify interfacing for oAuthV2 --> first interfacing with react client 
auth_spot = Blueprint('auth_spot', __name__)

#get data from config
PORT= os.getenv("FLASK_PORT")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = f"http://localhost:{PORT}/auth/callback"
SPOTIFY_SCOPES = 'user-read-email user-read-private user-top-read user-read-recently-played'  # Add other scopes if needed

authentication_request_params = {
            'response_type': 'code',
            'client_id': SPOTIFY_CLIENT_ID,
            'redirect_uri':SPOTIFY_REDIRECT_URI,
            'scope': SPOTIFY_SCOPES,
            'state': str(uuid.uuid4()),
            'show_dialog': 'true'
            }

#define function for each auth purpose
@auth_spot.route('/')
def index():
    return "This is an example app"

@auth_spot.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Store username and password in session for later use
    session['username'] = username
    session['password'] = password

    account = Account.query.filter_by(username=username).first()
    if not account:
        account = Account(username=username, password=password)
        db.session.add(account)
        db.session.commit()

        auth_url = 'https://accounts.spotify.com/authorize/?' + urllib.parse.urlencode(authentication_request_params), 201
        return jsonify({"auth_url": auth_url})
    elif account:
        user_data={"username": username, "user_id": account.id}
        access_token = create_access_token(identity=user_data)
        if account.authorized and account.check_password(password):
            return jsonify({"message": "account exist and has been authorized, welcome", "access_token": access_token}), 200
        elif not account.check_password(password):
            return jsonify({"message": "account exist and but credential is wrong, try again"}), 401
        elif not account.authorized:
            auth_url = 'https://accounts.spotify.com/authorize/?' + urllib.parse.urlencode(authentication_request_params)
            return jsonify({"message": "account exist and please wait for approval, or", "auth_url": auth_url}), 403  
         
        
@auth_spot.route('/callback')
def callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
        "scope": SPOTIFY_SCOPES
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    print(token_data)
    access_token = token_data['access_token']
    refresh_token = token_data.get('refresh_token', None)

    username = session.get('username')
    username = 'test2'

    account = Account.query.filter_by(username=username).first()
    existing_token = Token.query.filter_by(user_id=account.id).first()

    if existing_token:
        # Update the existing token with the new access and refresh tokens
        existing_token.access_token = access_token
        existing_token.refresh_token = refresh_token
    else:
        # If no existing token found, create a new one
        new_token = Token(
            token_expiration = datetime.now() + timedelta(seconds=token_data.get('expires_in')),
            access_token=access_token,
            refresh_token=refresh_token,
            username = username,
            user_id=account.id
        )
        db.session.add(new_token)

    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=access_token)
    }
    r = requests.get("https://api.spotify.com/v1/me/", headers = input_variables)
    user_data = r.json()
    print(user_data)

    profile = Profile.query.filter_by(spotifyid=user_data.get("id")).first()
    if not profile:
        new_profile = Profile(
            spotifyid=user_data.get("id"),
            email = user_data.get("email"),
            username = account.username
        )
        db.session.add(new_profile)

    account.authorized = True
    db.session.commit() 

    user_data={"username": username, "user_id": account.id}

    access_token = create_access_token(identity=user_data)

    return jsonify({"jwt_token": access_token})



