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

### Let's analize the key metrics of your fav songs

# Correlation between key metrics

fig=px.imshow(df.corr(),text_auto=True,height=800,width=800,color_continuous_scale=px.colors.sequential.Greens,aspect='auto',title='<b>paiwise correlation of columns')
fig.update_layout(title_x=0.5)
fig.show()

# Histograms by key metrics

fig=make_subplots(rows=3,cols=3,subplot_titles=('<i>DurationMS', '<i>Popularity', '<i>Acousticness', '<i>Danceability', '<i>Energy', '<i>Instrumentalness', '<i>Liveness', '<i>Loudness', '<i>Tempo'))
fig.add_trace(go.Histogram(x=df['DurationMS'],name='DurationMS'),row=1,col=1)
fig.add_trace(go.Histogram(x=df['Popularity'],name='Popularity'),row=1,col=2)
fig.add_trace(go.Histogram(x=df['Acousticness'],name='Acousticness'),row=1,col=3)
fig.add_trace(go.Histogram(x=df['Danceability'],name='Danceability'),row=2,col=1)
fig.add_trace(go.Histogram(x=df['Energy'],name='Energy'),row=2,col=2)
fig.add_trace(go.Histogram(x=df['Instrumentalness'],name='Instrumentalness'),row=2,col=3)
fig.add_trace(go.Histogram(x=df['Liveness'],name='Liveness'),row=3,col=1)
fig.add_trace(go.Histogram(x=df['Loudness'],name='Loudness'),row=3,col=2)
fig.add_trace(go.Histogram(x=df['Tempo'],name='Tempo'),row=3,col=3)
fig.update_layout(height=900,width=900,title_text='<b>Feature Distribution')
fig.update_layout(template='plotly_dark',title_x=0.5)
fig.show()


### Get similar artists by artist present in Oceanic

columns = ['Artist','Similar To']
data = []

for a in range(0,len(df)):
  json_artist_similar = sp.artist_related_artists(artist_id = df['ArtistId'][a])
  artists = json_artist_similar['artists']
  for i in artists:
    data.append([df['Artist'][a],i['name']])

df_similarities = pd.DataFrame(data,columns=columns)

# Data Wrangling. A name that bothers us, no offense tho.

mask = df_similarities['Similar To'] == 'Joey Bada$$'

# Eliminar las filas que cumplen con la máscara
df_similarities = df_similarities.drop(df_similarities[mask].index)


# Who's the most familiar between our top artists from Oceanic?

count_similar_to = df_similarities['Similar To'].value_counts()
df_similarities['CountSimilarTo'] = df_similarities['Similar To'].map(count_similar_to)

top_similar = count_similar_to[:20]
top_similar.index

plt.bar(top_similar.index, top_similar.values)
plt.show()

# Well, Spotify makes a big pressure on us with Barnes

df.to_csv('C:/Users/nicolas.alalu/OneDrive - ANALYTICALWAYS SL/Documentos/Documentos personales/DATAPROJECTS_/Spotify/TEST.csv',index=False)

