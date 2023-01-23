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


# read credentials from config file

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['spotify']['client_id']
client_secret = config['spotify']['client_secret']
spotipy_redirect_uri = config['spotify']['spotipy_redirect_uri']

# create spotipy connector

scope = 'user-read-recently-played'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=spotipy_redirect_uri,scope=scope))


### Get my most representative playlist called 'Oceanic's artists'

# Store playlist Id

playlist_id = '0VcSA1MBHoMH0onPpxHGWq'

 # Extract full json from Oceanic. Pagination navigation

def all_tracks(playlist_id):
    tracks_response = sp.playlist_tracks(playlist_id)
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response["items"])

    return tracks

json_oceanic = all_tracks(playlist_id)

# Prepare the data and columns for future storage

columns = ['ArtistId','Name','Album','Artist','ReleasedDate','AddedAt','DurationMS','Popularity','Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Tempo']
data = []

### Extract

for i in range(0,len(json_oceanic)):
  song_id = json_oceanic[i]['track']['id']
  json_audio_features = sp.audio_features(song_id)
  artist_id = json_oceanic[i]['track']['artists'][0]['id']
  song = json_oceanic[i]['track']['name']
  album = json_oceanic[i]['track']['album']['name']
  artist = json_oceanic[i]['track']['artists'][0]['name']
  released_date = json_oceanic[i]['track']['album']['release_date']
  added_at = json_oceanic[i]['added_at']
  duration_ms = json_oceanic[i]['track']['duration_ms']
  popularity = json_oceanic[i]['track']['popularity']
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

df.to_csv(,index=False)

