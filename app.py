from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import os
import uuid
import urllib
import webbrowser
from dotenv import load_dotenv
import jwt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
PORT = 8000

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = f"http://localhost:{PORT}/callback"
SPOTIFY_SCOPES = 'user-read-email user-read-private user-top-read user-read-recently-played'  # Add other scopes if needed
JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route('/login')
def login():
    authentication_request_params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'redirect_uri':SPOTIFY_REDIRECT_URI,
        'scope': SPOTIFY_SCOPES,
        'state': str(uuid.uuid4()),
        'show_dialog': 'true'
        }

    auth_url = 'https://accounts.spotify.com/authorize/?' + urllib.parse.urlencode(authentication_request_params)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    print(code)
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
    access_token = token_data['access_token']
    jwt_token = jwt.encode({"access_token": access_token}, JWT_SECRET_KEY, algorithm="HS256")

    #might need to comment out
    session["jwt_token"]=jwt_token

    return jsonify({"jwt_token": jwt_token})

@app.route("/get_most_recent")
def get_most_recent():
    jwt_token = session.get("jwt_token")
    print(jwt_token)

    if jwt_token:
        try:
            # Decode and verify the JWT token
            decoded_token = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=["HS256"])
            access_token = decoded_token.get("access_token")

            if access_token:
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("items"):
                        most_recent_track = data["items"][0]["track"]["name"]
                        return f"Most Recently Played Track: {most_recent_track}"
                    else:
                        return "No recently played tracks found"
        except jwt.ExpiredSignatureError:
            return "JWT token expired"
        except jwt.DecodeError:
            return "Invalid JWT token"
    else:
        return "JWT token not found or invalid"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
