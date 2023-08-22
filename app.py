from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import os
import uuid
import urllib
import webbrowser
from dotenv import load_dotenv
import jwt

from auth_spot import auth_spot
from db_query import db_query
from etl import etl

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.register_blueprint(auth_spot.auth_spot, url_prefix='/auth')
app.register_blueprint(db_query.db_query, url_prefix='/dbquery')
app.register_blueprint(etl.etl, url_prefix='/etl')

PORT = os.getenv('FLASK_PORT')

if __name__ == "__main__":
    app.run(debug=True, port=PORT,threaded=True)
