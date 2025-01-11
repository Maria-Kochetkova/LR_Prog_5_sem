import unittest
from unittest.mock import patch
from getweatherdata import get_weather_data
from mykey import key


class TestGetWeatherData(unittest.TestCase):

    @patch('requests.get')
    def test_successful_response_moscow(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'name': 'Moscow',
            'coord': {'lon': 37.6156, 'lat': 55.7522},
            'sys': {'country': 'RU'},
            'timezone': 10800,
            'main': {'feels_like': 1.62}
        }

        result = get_weather_data('Moscow', key)

        expected_result = '''{
    "name": "Moscow",
    "coord": {
        "lon": 37.6156,
        "lat": 55.7522
    },
    "country": "RU",
    "timezone": "UTC+3",
    "feels_like": 1.62
}'''

        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_successful_response_newyork(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'name': 'New York',
            'coord': {'lon': -74.006, 'lat': 40.7143},
            'sys': {'country': 'US'},
            'timezone': -18000,
            'main': {'feels_like': -1.11}
        }

        result = get_weather_data('New York', key)

        expected_result = '''{
    "name": "New York",
    "coord": {
        "lon": -74.006,
        "lat": 40.7143
    },
    "country": "US",
    "timezone": "UTC-5",
    "feels_like": -1.11
}'''
        self.assertEqual(result, expected_result)

    def test_invalid_city_name(self):
        with self.assertRaises(ValueError):
            get_weather_data('', key)

    def test_api_error_response(self):
        with self.assertRaises(ValueError):
            get_weather_data('InvalidCity', key)

    def test_none_api_key(self):
        with self.assertRaises(ValueError):
            get_weather_data('Moscow', None)

    def test_invalid_api_key(self):
        with self.assertRaises(ValueError):
            get_weather_data('Moscow', 'invalid_key')

if __name__ == '__main__':
    unittest.main()
