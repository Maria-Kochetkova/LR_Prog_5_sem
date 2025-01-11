import requests
import json
from mykey import key


def utc_timezone(time):
    t = time // 3600
    return f"UTC{'+' if t >= 0 else ''}{t}"

def get_weather_data(city_name, api_key=None):

    if not isinstance(city_name, str) or not city_name.strip():
        raise ValueError("Аргумент 'city_name' должен быть непустой строкой.")

    if api_key is None:
        raise ValueError("Аргумент 'api_key' не может быть None.")

    if api_key != key:
        raise ValueError("Неверный API key.")

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    requests_data = requests.get(url).json()

    if 'name' not in requests_data or requests_data['name'].lower() != city_name.lower():
        raise ValueError("Город не найден.")

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

    return json_data
