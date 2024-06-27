from api_key import *
from genre_database import *
import openai
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
from spotify_genres import genres

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GPT_API_KEY = os.getenv('GPT_API_KEY')


# function to welcome the user
def welcome_user():
    print("Welcome to WeatherTunes! 🌤️  🎶")
    print("Discover the perfect soundtrack for your day with personalized song suggestions based on the weather and your activities.🌸")
    print("Let the Music Match the Mood! 😎")
    return True


# function to get weather forecast for a specified city
def weather_forecast():
    correct_city = False
    while not correct_city:
        city = input("Enter your city: ")
        # WEATHER_API_KEY = get_weather_api_key()
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()
            city_from_response = json_response['location']['name']
            region_from_response = json_response['location']['region']
            print(f"Is {city_from_response} in {region_from_response} your desired location?")
            while True:
                proper_location = input("Type 'y' if it is correct and 'n' to input a new location: ").strip().lower()
                if proper_location == 'y':
                    correct_city = True
                    break
                elif proper_location == 'n':
                    break
                else:
                    print("Invalid Entry: enter 'y' or 'n'")
        else:
            print("Error, status code:", response.status_code)
            print("Please try again with a valid city name")

    if correct_city:
        fahrenheit = json_response['current']['temp_f']
        weather = json_response['current']['condition']['text']
        return [fahrenheit, weather], city


# function to get user's activity
def users_activity():
    while True:
        activity = input("In a few words, what activity will you be doing (limit 50 characters)? ")
        if len(activity) <= 50:
            return activity
        else:
            print("Character limit exceeded. Please enter the activity again with a shorter description")


# function to get query words from chat GPT's API
def gpt_query_words():
    # GPT_API_KEY = get_gpt_api_key()

    # create an OpenAPI client using the key from our environment variable
    client = OpenAI(
        api_key=GPT_API_KEY,
    )

    # Specify the model to use and the messages to send
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a muiscal genius that generates a list of 5 words or short phrases to use in the Spotify API search function based on the given activity and weather."},
            {"role": "user", "content": f"The weather is {weather_stats[0]} degrees and {weather_stats[1]} and the activity is {activity}"}
        ]
    )
    return (completion.choices[0].message.content)


# function to get a list of songs from a specific genre
def get_songs_from_genre():
    while True:
        show_genres = show_genre_list()
        if show_genres:
            print(list_of_genres())
        genre_table = (input("So what genre are you feeling? "))
        if genre_table in genres:
            formatted_genre = (genre_table.lower()).replace("-", "")
            with engine.connect() as connection:
                query_result = connection.execute(db.text(f"SELECT * FROM {formatted_genre};")).fetchall()
                return query_result
        else:
            print("Invalid genre. Please try again.")


# function to see if the user wants to see a list of genres
def show_genre_list():
    while True:
        genre_list_request = input("Would you like to see a list of possible genres? Type 'y' if yes and 'n' if no: ")
        if genre_list_request == 'y':
            return True
        elif genre_list_request == 'n':
            return False
        else:
            print("Invalid Entry: enter 'y' or 'n'")


# function to show the user a list of genres
def list_of_genres():
    return genres


# function to give the user the songs and send closing messages
def final_response(activity, city, weather_stats, songs):
    while True:
        more_info = input("Would you like to see the basic info or extended info for each song? Type 'b' for basic and 'e' for extended: ")
        if more_info == 'b':
            print(f"\nI hope you enjoy {activity} in {city} 😁")
            print(f"It will be around {weather_stats[0]} degrees and {weather_stats[1]}.")
            print("Here are some tunes to groove to:")
            for i in range(len(songs)):
                print(f"{i+1}. {songs[i][1]} by {songs[i][2]}. 🎶")
            break
        elif more_info == 'e':
            print(f"\nI hope you enjoy {activity} in {city} 😁")
            print(f"It will be around {weather_stats[0]} degrees and {weather_stats[1]}.")
            print("Here are some tunes to groove to:")
            for i in range(len(songs)):
                print(f"{i+1}. {songs[i][1]} by {songs[i][2]} from {songs[i][3]}. 🎶")
                print(f"Song Link: {songs[i][4]}\n")
            break
        else:
            print("Invalid Entry: enter 'b' or 'e'")

    while True:
        see_another_genre = input("Would you like to see similar songs from another genre? Type 'y' for yes or 'n' for no: ")
        if see_another_genre == 'y':
            songs = get_songs_from_genre()
            final_response(activity, city, weather_stats, songs)
        elif see_another_genre == 'n':
            print("Awesome, enjoy your day with some great music! 🌟")
            exit()
        else:
            print("Invalid Entry: enter 'y' or 'n'")
    return True


# main function
if __name__ == "__main__":
    welcome_user()
    weather_stats, city = weather_forecast()
    if (isinstance(weather_stats, list)):
        activity = users_activity()
        query_words = gpt_query_words()
        print("Ok, let me cook for a little bit.\n")
        create_db(query_words)
        print("Ok great! I thought of some songs for many genres, let's narrow it down for you.")
        songs = get_songs_from_genre()
        final_response(activity, city, weather_stats, songs)
