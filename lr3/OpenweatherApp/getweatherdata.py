import requests
import json

def utc_timezone(time):
    t = time // 3600
    return f"UTC{'+' if t >= 0 else ''}{t}"

def get_weather_data(city_name, api_key=None):

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    requests_data = requests.get(url).json()

    data = {
        'name': requests_data['name'],
        'coord': {
            'lon': requests_data['coord']['lon'],
            'lat': requests_data['coord']['lat']
        },
        'country': requests_data['sys']['country'],
        'timezone': utc_timezone(requests_data['timezone']),
        'feels_like': requests_data['main']['feels_like']
    }

    json_data = json.dumps(data, indent=4)

    print(json_data)