from urllib.parse import urlencode
import requests

class OpenWeatherMapAPI():
    URL = 'https://api.openweathermap.org/data/2.5/onecall?'
    UNITS = 'metric'
    API_KEY = 'bd5e378503939ddaee76f12ad7a97608'
    EXCLUDES = ['current', 'minutely', 'hourly', 'alerts']
    expected_status_code = 200
    account_blocked_status_code = 429

    @classmethod
    def get_response_from_city(cls, city):
        params = {
            'lat': city.latitude,
            'lon': city.longitude,
            'exclude': ','.join(cls.EXCLUDES),
            'appid': cls.API_KEY,
            'units': cls.UNITS
        }
        
        query_string = urlencode(params)
        url = f"{cls.URL}{query_string}"
        return requests.get(url)

class ReservamosAPI():
    URL = 'https://search.reservamos.mx/api/v2/places?q='
    expected_status_code = 201

    @classmethod
    def get_response_from_city_name(cls, city: str):
        url = f"{cls.URL}{city}"
        return requests.get(url)