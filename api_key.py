import requests
import os
from dotenv import load_dotenv

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def get_spotify_api_key():
    CLIENT_ID = SPOTIFY_CLIENT_ID
    CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

    AUTH_URL = "https://accounts.spotify.com/api/token"

    auth_response = requests.post(AUTH_URL, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    return auth_response_data["access_token"]
