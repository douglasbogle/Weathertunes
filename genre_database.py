import pandas as pd
import sqlalchemy as db
from spotify_genres import genres
from api_key import *


engine = db.create_engine('sqlite:///music_info.db')  # create database file


def create_db(query_words):
    SPOTIFY_API_KEY = get_spotify_api_key()
    headers = {"Authorization": "Bearer {token}".format(token=SPOTIFY_API_KEY)}

    for genre in genres:  # make a database table for every genre we have
        final_query = f"{genre} {' '.join(query_words)}"
        params = {
            "q": final_query,
            "type": "track",
            "limit": 5
        }

        response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
        data = response.json()
        songs_dict = {}

        for i, item in enumerate(data['tracks']['items']):  # put all songs of one genre into dict
            song_name = item['name']
            artist_name = item['artists'][0]['name']
            album_name = item['album']['name']
            song_link = item['external_urls']['spotify']
            songs_dict[i + 1] = {"song_name": song_name, "artist_name": artist_name, "album_name": album_name, "song_link": song_link}

        dict_to_table(songs_dict, genre.replace(("-"), ""))  # create an sql table for this genre, remove - character as it causes errors


def dict_to_table(genre_dict, genre):
    df = pd.DataFrame.from_dict(genre_dict, orient='index')
    df.to_sql(genre, con=engine, if_exists='replace')  # create a singular genre table in our already made database
