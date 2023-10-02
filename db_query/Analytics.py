import pandas as pd
from datetime import datetime

def top_songs(song_history):
    top_songs = song_history['song_name'].value_counts().reset_index()
    top_songs.columns = ['song_name', 'count']
    top_songs = top_songs.head(5)
    top_songs_dict = top_songs.set_index('song_name')['count'].to_dict()

    return top_songs_dict

def get_listening_pattern (song_history):
    song_history_df = pd.DataFrame(song_history)
    # Convert 'timestamp' column to datetime
    song_history_df['played_at'] = pd.to_datetime(song_history_df['played_at'])
    song_history_df['hour'] = song_history_df['played_at'].dt.hour
    song_count_by_hour = song_history_df.groupby('hour').size().to_dict()

    listening_hours_dict = {hour: 0 for hour in range(24)}
    listening_hours_dict.update(song_count_by_hour)
    threshold = int(len(listening_hours_dict) * 0.1)

    # Get the top listened hours
    top_hours = dict(sorted(listening_hours_dict.items(), key=lambda x: x[1], reverse=True)[:threshold])
    return listening_hours_dict, top_hours


def listening_analytics(song_history):
    top_songs_dict = top_songs(song_history)
    unique_songs = song_history['song_name'].nunique()
    listening_hours_dict, top_hours = get_listening_pattern(song_history)

    return top_songs_dict, unique_songs, listening_hours_dict, top_hours