import pandas as pd 
import requests
from datetime import datetime
import datetime
import json

#temporarily initialize token: to be ported over to airflow function
try:
    with open('shared_variable.json', 'r') as json_file:
        data = json.load(json_file)
        token = data['access_token']
except Exception as e:
    token='' 

def get_user_profile():
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=token)
    }
    r = requests.get("https://api.spotify.com/v1/me/", headers = input_variables)
    data = r.json()
    profile_dict = {
        "name" : [data['display_name']],
        "email": [data['email']],
        "public": True if data['display_name']=='Victorlim' else False
    }
    profile_df = pd.DataFrame(profile_dict, columns = ["name", "email","public"])
    return profile_df
    

# Creating an function to be used in other python files
def get_listen_history(): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=token)
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=10) #no of Days u want the data for)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    profile= get_user_profile()
    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    response = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)

    data = response.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    spotify_id=[]

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        song_names.append(song["track"]["name"])
        timestamps.append(song["played_at"][0:10])
        played_at_list.append(song["played_at"])
        spotify_id.append(song['track']["id"])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "name": profile['name'][0],
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps,
        "spotify_id": spotify_id,
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp","name", "spotify_id"])
    return song_df

#to create dataframe for song metrics
def get_song_metrics(song_df):
    id_list= song_df['spotify_id'].unique()
    response= metrics_query(id_list)
    #specifying which parameter to take:
    metric_df = pd.DataFrame(response, columns=["id","danceability","energy","key","loudness","tempo","liveness","speechiness","acousticness"])
    metric_df= metric_df.rename(columns={
        "id": "spotify_id"})
    return metric_df

#helper for query function
def metrics_query(track_ids):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/audio-features/?ids={','.join(track_ids)}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["audio_features"]
