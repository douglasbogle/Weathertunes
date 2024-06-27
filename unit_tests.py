import unittest
from unittest.mock import patch
from weather_tunes import *

class UnitTests(unittest.TestCase):
    def test_welcome_user(self):
        self.assertEqual(welcome_user(), True)

    @patch('builtins.input', side_effect=['Houston', 'y'])  # all this does is autofill the function's call for input
    def test_weather_forecast(self, mock_input):
        weather, place = weather_forecast()
        self.assertIsInstance(weather, list)
        self.assertIsInstance(place, str)


    @patch('builtins.input', side_effect="Doing insane backflips")  # all this does is autofill the function's call for input
    def test_users_activity(self, mock_input):
        keywords = users_activity()
        self.assertIsInstance(keywords, str)


    @patch('builtins.input', side_effect=["n", "hip-hop"])  # all this does is autofill the function's call for input
    def test_get_songs_from_genre(self, mock_input):
        songs = get_songs_from_genre()
        self.assertIsInstance(songs, list)

    @patch('builtins.input', side_effect="y")  # all this does is autofill the function's call for input
    def test_show_genre_list(self, mock_input):
        self.assertEqual(show_genre_list(), True)


if __name__ == '__main__':
    unittest.main()
