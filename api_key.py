import requests

def get_weather_api_key():
    return 'c152661085b946e0ab8184515242406'

def get_gpt_api_key():
    return 'sk-proj-qTd5Ntrt7pEdCb6PWXUST3BlbkFJLqPt1czpnI7l5VU3jpV1'

def get_spotify_api_key():
    CLIENT_ID = "3774bb536c9e42ed86976e60befb4d28"
    CLIENT_SECRET = "71a181b61bf84bef800b300d32d852ba"

    AUTH_URL = "https://accounts.spotify.com/api/token"

    auth_response = requests.post(AUTH_URL, {
        "grant_type": "client_credentials", 
        "client_id": CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    return auth_response_data["access_token"]
    