from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import os
import uuid
import urllib
import webbrowser
from dotenv import load_dotenv
import jwt

from auth_spot import auth_spot

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(auth_spot.auth_spot, url_prefix='/auth')

PORT = os.getenv('FLASK_PORT')

if __name__ == "__main__":
    app.run(debug=True, port=PORT,threaded=True)
