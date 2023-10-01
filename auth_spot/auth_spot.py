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

##import utils for decode
from utils.utils import *
from models.user import Account 
from models.token import Token  

from app import db

##Define blueprint to be registered in the main app
##AUTH route is mainly for spotify interfacing for oAuthV2 --> first interfacing with react client 
auth_spot = Blueprint('auth_spot', __name__)

#get data from config
PORT= os.getenv("FLASK_PORT")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = f"http://localhost:{PORT}/auth/callback"
SPOTIFY_SCOPES = 'user-read-email user-read-private user-top-read user-read-recently-played'  # Add other scopes if needed

access_token=''

#define function for each auth purpose
@auth_spot.route('/')
def index():
    return "This is an example app"

@auth_spot.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Store username and password in session for later use
    session['username'] = username
    session['password'] = password

    authentication_request_params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'redirect_uri':SPOTIFY_REDIRECT_URI,
        'scope': SPOTIFY_SCOPES,
        'state': str(uuid.uuid4()),
        'show_dialog': 'true'
        }

    auth_url = 'https://accounts.spotify.com/authorize/?' + urllib.parse.urlencode(authentication_request_params)
    return jsonify({"jwt_token": auth_url})

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
    password = session.get('password')
    print(username)
    username='test3'
    password='test'

    account = Account.query.filter_by(username=username).first()
    if not account:
        account = Account(username=username, password=password)
        db.session.add(account)
        db.session.commit()

    user_id = account.id
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id  # Use the user's ID to link the token to the user
    )
    
    db.session.add(token)
    db.session.commit()

    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=access_token)
    }
    r = requests.get("https://api.spotify.com/v1/me/", headers = input_variables)
    user_data = r.json()
    print(user_data)

    ##store in json file
    json_file_path = 'access_token.json'

    try:
    # Open the JSON file for reading
        with open(json_file_path, 'r') as json_file:
            user_token = json.load(json_file)
    except FileNotFoundError:
    # If the file doesn't exist, create an empty dictionary
            user_token = {}
    #randomly generate token for reference code
    reference_code = secrets.token_hex(16)
    user_token[reference_code]=access_token

    #update values
    with open('access_token.json', 'w') as json_file:
        json.dump(user_token, json_file, indent=4)

    payload = {"reference_token": reference_code, "user":user_data['display_name'], "email": user_data['email'] }

    jwt_token = generate_token(payload)
    decoded_token = verify_token(jwt_token)

    #might need to comment out
    session["jwt_token"]=jwt_token

    return jsonify({"jwt_token": jwt_token})



