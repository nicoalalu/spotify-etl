# Spotify Playlist Analyzer

Analyze your Spotify playlists automatically with this code!

This code uses the "configparser" library to read credentials from a configuration file called "config.ini". It is necessary for the config.ini file to be in the same directory as the script and to have the following sections and parameters:

------------------------

[spotify]
- client_id=your_client_id
- client_secret=your_client_secret
- spotipy_redirect_uri=your_redirect_uri

------------------------
To learn how the Spotify API works with its respective parameters, here is the [documentation](https://developer.spotify.com/documentation/web-api/).


Before using this code, it is necessary to have a registered user on Spotify and an application created on the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications) to obtain the necessary credentials (client_id and client_secret) and place them in the config.ini file and a valid redirect URL to place in the spotipy_redirect_uri section of the config.ini file

*It's important to note that these credentials are sensitive information, so it's extremely important to not share them with anyone for security reasons.*

Once configured, the code uses the "spotipy" library to connect to the Spotify API with those credentials and a specific scope of "user-read-recently-played".

This code is used to obtain and store information about songs in a specific playlist and their audio features in a pandas DataFrame for further analysis. You will be able to know which songs are the most popular, acoustic, danceable, and more!

## Requirements

* python 3.6 or higher
* spotipy 2.13.0 or higher
* pandas 1.1.4 or higher
* configparser 3.8.1 or higher

**Let the game begin!**
