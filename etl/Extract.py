import pandas as pd 
import requests
from datetime import datetime
import datetime
import json 
import pytz

def get_user_profile(token):
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
def get_listen_history(token, spotifyid): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=token)
    }
     
    local_timezone = pytz.timezone('Asia/Singapore')
    
    # Get the current time in the local timezone
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=2) #no of Days u want the data for)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    response = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)

    data = response.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    song_id=[]

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        song_names.append(song["track"]["name"])
        timestamps.append(song["played_at"][0:10])
        played_at = datetime.datetime.strptime(song["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        played_at = played_at.replace(tzinfo=pytz.utc)  # Set the timezone of the timestamp to UTC
        played_at = played_at.astimezone(local_timezone)  # Convert it to the local timezone
        played_at_list.append(played_at.strftime("%Y-%m-%d %H:%M:%S"))
        song_id.append(song['track']["id"])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "spotifyid": spotifyid,
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps,
        "song_id": song_id,
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp","spotifyid", "song_id"])
    return song_df

#to create dataframe for song metrics
def get_song_metrics(song_df, token):
    song_df= song_df[['song_id',"song_name"]]
    id_list= song_df['song_id'].unique()
    response= metrics_query(id_list, token)
    #specifying which parameter to take:
    metric_df = pd.DataFrame(response, columns=["id","danceability","energy","key","loudness","tempo","liveness","speechiness","acousticness"])
    metric_df= metric_df.rename(columns={"id": "song_id"})
    metric_df= pd.merge(song_df, metric_df, on='song_id',how='left')
    metric_df= metric_df.drop_duplicates()
    return metric_df

#helper for query function
def metrics_query(track_ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/audio-features/?ids={','.join(track_ids)}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["audio_features"]
