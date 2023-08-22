from flask import session, Blueprint, request, jsonify, redirect
import requests
import os
import uuid
import urllib
import webbrowser
from dotenv import load_dotenv
import jwt
import json
import sqlite3
import sqlalchemy
from sqlalchemy.orm import sessionmaker

db_query = Blueprint('db_query', __name__)
JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')


def get_db_connection():
    conn = sqlite3.connect('./tracks_analytics.db')
    conn.row_factory = sqlite3.Row 
    print(conn)
    return conn

@db_query.route('/getUser')
def get_user():
    conn = get_db_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM fav_artist LIMIT 30")  
    users = [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries
    conn.close()
    return jsonify(users)

