from urllib.parse import urlencode
import requests

class OpenWeatherMapAPI():
    """
    This class is to work with the openweathermap api.

    Attributes:
        URL (str): The url of the openweathermap api.
        UNITS (str): The units to use in the api.
        API_KEY (str): The api key to use in the api.
        EXCLUDES (list): The excludes to use in the api.
        expected_status_code (int): The expected status code to receive from the api.
        account_blocked_status_code (int): The status code that the api returns when the account is blocked.
    
    Methods:
        get_response_from_city: get the response from the api from the city provided.
    """
    URL = 'https://api.openweathermap.org/data/2.5/onecall?'
    UNITS = 'metric'
    API_KEY = 'a5a47c18197737e8eeca634cd6acb581'
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
    """
    This class is to work with the reservamos api.

    Attributes:
        URL (str): The url of the reservamos api.
        expected_status_code (int): The expected status code to receive from the api.
    
    Methods:
        get_response_from_city_name: get the response from the api from the city name provided.
    """
    URL = 'https://search.reservamos.mx/api/v2/places?q='
    expected_status_code = 201

    @classmethod
    def get_response_from_city_name(cls, city: str):
        url = f"{cls.URL}{city}"
        return requests.get(url)