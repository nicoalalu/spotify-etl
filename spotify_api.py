import configparser
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import networkx as nx
import matplotlib.pyplot as plt
import scipy
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3


# read the Spotify credentials from config file

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['spotify']['client_id']
client_secret = config['spotify']['client_secret']
spotipy_redirect_uri = config['spotify']['spotipy_redirect_uri']
playlist_id = config['spotify']['playlist_id']

# Read the path from the config file

file_path = config['general']['file_path']

# create spotipy connector

scope = 'user-read-recently-played'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=spotipy_redirect_uri,scope=scope))


### Get my most representative playlist from Spotify

# Extract full json from your favourite playlist using pagination navigation

def all_tracks(playlist_id):
    tracks_response = sp.playlist_tracks(playlist_id)
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response["items"])

    return tracks

json_playlist = all_tracks(playlist_id)

# Prepare the data and columns for future storage

columns = ['ArtistId','Name','Album','Artist','ReleasedDate','AddedAt','DurationMS','Popularity','Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Tempo']
data = []

### Extract

for i in range(0,len(json_playlist)):
  song_id = json_playlist[i]['track']['id']
  json_audio_features = sp.audio_features(song_id)
  artist_id = json_playlist[i]['track']['artists'][0]['id']
  song = json_playlist[i]['track']['name']
  album = json_playlist[i]['track']['album']['name']
  artist = json_playlist[i]['track']['artists'][0]['name']
  released_date = json_playlist[i]['track']['album']['release_date']
  added_at = json_playlist[i]['added_at']
  duration_ms = json_playlist[i]['track']['duration_ms']
  popularity = json_playlist[i]['track']['popularity']
  acousticness = json_audio_features[0]['acousticness']
  danceability = json_audio_features[0]['danceability']
  energy = json_audio_features[0]['energy']
  instrumentalness = json_audio_features[0]['instrumentalness']
  liveness = json_audio_features[0]['liveness']
  loudness = json_audio_features[0]['loudness']
  speechiness = json_audio_features[0]['speechiness']
  tempo = json_audio_features[0]['tempo']
  
  data.append([artist_id,song,album,artist,released_date,added_at,duration_ms,popularity,acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,tempo])

df = pd.DataFrame(data,columns=columns)

df.to_csv(file_path,index=False)

