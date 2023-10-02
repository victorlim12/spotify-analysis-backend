# Data Models

This section describes the data models used in our application to structure and manage data in the database.

## MyPlayedTrack

- **Table Name:** played_tracks
- **Attributes:**
  - `song_name` (String): The name of the played song.
  - `artist_name` (String): The name of the artist of the played song.
  - `played_at` (String, Primary Key, Unique): The timestamp of when the song was played. This uniquely identifies a play.
  - `timestamp` (String): A timestamp related to the play.
  - `spotifyid` (String, Foreign Key): The Spotify ID associated with the play.
  - `song_id` (String, Primary Key, Unique): Unique identifier for the song.

## Profile

- **Table Name:** Profile
- **Attributes:**
  - `id` (Integer, Primary Key, Autoincrement): Unique identifier for a profile.
  - `username` (String): The username associated with the profile (unique).
  - `spotifyid` (String, Unique): The Spotify ID associated with the profile (unique).
  - `email` (String, Unique): The email address associated with the profile (unique).

## Metric

- **Table Name:** track_metrics
- **Attributes:**
  - `song_id` (String, Primary Key, Unique): Unique identifier for a song's metrics.
  - `song_name` (String): The name of the song.
  - `danceability` (Float): A metric indicating danceability.
  - `energy` (Float): A metric indicating energy.
  - `key` (Integer): A metric indicating the musical key.
  - `loudness` (Float): A metric indicating loudness.
  - `tempo` (Float): A metric indicating tempo.
  - `liveness` (Float): A metric indicating liveness.
  - `speechiness` (Float): A metric indicating speechiness.
  - `acousticness` (Float): A metric indicating acousticness.

## Token

- **Table Name:** Token
- **Attributes:**
  - `id` (Integer, Primary Key): Unique identifier for a token.
  - `access_token` (String): Access token used for authentication.
  - `refresh_token` (String): Refresh token used to obtain a new access token.
  - `user_id` (Integer, Foreign Key): The user associated with the token.
  - `username` (String): The username associated with the token.
  - `token_expiration` (DateTime): Timestamp indicating when the access token expires.
  - `last_refreshed` (DateTime, Default: Current Timestamp): Timestamp indicating when the token was last refreshed.

## Account

- **Table Name:** Account
- **Attributes:**
  - `id` (Integer, Primary Key, Autoincrement): Unique identifier for an account.
  - `username` (String, Unique): The username associated with the account (unique).
  - `password_hash` (String): The hashed password for the account.
  - `salt` (String): A unique salt used in password hashing.
  - `authorized` (Boolean, Default: False): Indicates if the account is authorized.
  
