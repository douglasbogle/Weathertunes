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


def welcome_user():
    """
    Function to get weather forecast for a specified city.
    """
    print("Welcome to WeatherTunes! 🌤️  🎶")
    print("Discover the perfect soundtrack for your day with personalized song suggestions based on the weather and your activities.🌸")
    print("Let the Music Match the Mood! 😎")
    return True


def weather_forecast():
    """
    Function to get weather forecast for a specified city.
    """
    correct_city = False
    while not correct_city:
        city = input("Enter your city: ")
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


def users_activity():
    """
    Function to get user's activity.
    """
    while True:
        activity = input("In a few words, what activity will you be doing (limit 50 characters)? ")
        if len(activity) <= 50:
            return activity
        else:
            print("Character limit exceeded. Please enter the activity again with a shorter description")



def gpt_query_words():
    """
    Function to get query words from OpenAI's GPT-3.5 API based on weather and activity.
    """

    # create an OpenAPI client using the key from our environment variable
    client = OpenAI(
        api_key=GPT_API_KEY,
    )

    # Specifying the model to use and the messages to send
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a muiscal genius that generates a list of 5 words or short phrases to use in the Spotify API search function based on the given activity and weather."},
            {"role": "user", "content": f"The weather is {weather_stats[0]} degrees and {weather_stats[1]} and the activity is {activity}"}
        ]
    )
    return (completion.choices[0].message.content)


def get_songs_from_genre():
    """
    Function to get a list of songs from a specific genre.
    """
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


def show_genre_list():
    """
    Function to ask if the user wants to see a list of genres.
    """
    while True:
        genre_list_request = input("Would you like to see a list of possible genres? Type 'y' if yes and 'n' if no: ")
        if genre_list_request == 'y':
            return True
        elif genre_list_request == 'n':
            return False
        else:
            print("Invalid Entry: enter 'y' or 'n'")


def list_of_genres():
    return genres


def final_response(activity, city, weather_stats, songs):
    """
    Function to present final response to the user, displaying songs and handling further user interactions.
    """
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
