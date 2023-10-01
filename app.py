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

from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True

    # Import and register blueprints here
    from auth_spot.auth_spot import auth_spot
    from db_query.db_query import db_query
    from etl.etl import etl

    app.register_blueprint(auth_spot, url_prefix='/auth')
    app.register_blueprint(db_query, url_prefix='/dbquery')
    app.register_blueprint(etl, url_prefix='/etl')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            db.init_app(app)
            from app import db

            db.create_all()

            # Commit the changes to the database
            db.session.commit()
        except Exception as e:
            print(e)
    app.run(debug=True, port=os.getenv('FLASK_PORT'), threaded=True)
