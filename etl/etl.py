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
from etl.Load import Load_sqlite

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
@etl.route('/')
def run_etl():
    try:
        token_client = request.headers.get('Authorization').split()[1]
        payload= verify_token(token_client)
        print(payload['email'])
        with open(json_file_path, 'r') as json_file:
            user_token = json.load(json_file)
            access_token= user_token[payload['reference_token']]
            response = Load_sqlite(access_token)
        if response.json["code"]==200:
             return jsonify({'message': 'ETL completed, time to go query', 'code': 200})
        else:
            return jsonify({'message': f'ETL failed, error: {response.json["message"]}', 'code': 500})
    except Exception as e:
        return jsonify({'message': f'error found: {e}', 'code': 404})
    
# @etl.route('/analytics')
# def run_analytics();
#     return jsonify({'message': 'ETL completed, time to go query', 'code': 200})




