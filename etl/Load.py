from etl import Extract, Transform
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from flask import jsonify

#database engine location
DATABASE_LOCATION = "sqlite:///tracks_analytics.db"

def Load_sqlite(access_token):
    try:
        token=access_token
        print(token)
        #Importing the songs_df from the Extract.py
        load_df=Extract.get_listen_history(token)
        if(Transform.Data_Quality(load_df) == False):
            raise ("Failed at Data Validation")
        
        metric_df=Extract.get_song_metrics(load_df, token)
        Transformed_df=Transform.Transform_df(load_df)
        profile_df=Extract.get_user_profile(token)

        print(metric_df)

        #Loading into Database
        engine = sqlalchemy.create_engine(DATABASE_LOCATION)
        conn = sqlite3.connect('./tracks_analytics.db')
        cursor = conn.cursor()

        #SQL Query to Create Played Songs
        sql_query_1 = """
        CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            name VARCHAR(200),
            spotify_id VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at, spotify_id)
        )
        """
        #SQL Query to Create Most Listened Artist
        sql_query_2 = """
        CREATE TABLE IF NOT EXISTS fav_artist(
            timestamp VARCHAR(200),
            ID VARCHAR(200),
            artist_name VARCHAR(200),
            count VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
        )
        """
        #Create User Table
        sql_query_3 = """
        CREATE TABLE IF NOT EXISTS user_table(
            name VARCHAR(200),
            email VARCHAR(200),
            public BOOLEAN,
            CONSTRAINT primary_key_constraint PRIMARY KEY (name, email)
        )
    """
        sql_query_4 = """
            CREATE TABLE IF NOT EXISTS metric_table(
                spotify_id VARCHAR(200),
                song_name VARCHAR(200),
                danceability FLOAT,
                energy FLOAT,
                key INTEGER,
                loudness FLOAT,
                tempo FLOAT,
                liveness FLOAT,
                speechiness FLOAT,
                acousticness FLOAT,
                CONSTRAINT primary_key_constraint PRIMARY KEY (spotify_id)
            )
        """
        cursor.execute(sql_query_1)
        cursor.execute(sql_query_2)
        cursor.execute(sql_query_3)
        cursor.execute(sql_query_4)
        print("Opened database successfully")
        
        #We need to only Append New Data to avoid duplicates
        try:
            load_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
        except:
            print("Data already exists in the song database")
        try:
            Transformed_df.to_sql("fav_artist", engine, index=False, if_exists='append')
        except:
            print("Data already exists in the artist database")
        try:
            profile_df.to_sql("user_table", engine, index=False, if_exists='append')
        except:
            print("Data already exists in the profile database")
        try:
            metric_df.to_sql("metric_table", engine, index=False, if_exists='append')
        except:
            print("Data already exists in the metric database")


        conn.close()
        return jsonify({"message": 'loading performed successfully', "code":200})
    except Exception as e:
        return jsonify({"message": f'loading failed, error: {e}', "code":500})