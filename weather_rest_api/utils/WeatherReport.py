from weather_rest_api.models import City, TemperatureReport
from .apis import OpenWeatherMapAPI

import json

class WeatherReport():
    """
    Class to manage the weather report of the cities.
    
    attributes:
        key_to_search_for_report: key to search for the weather report in the json response from openweathermap api.
        maximum_temperature_values_to_store: maximum temperature values to store in the weather report.
        cities: cities of the weather report.
    
    methods:
        add_city: add city to the weather report.
        get_cities: get the cities of the weather report.
        get_cities_report_as_dict: get the cities report as dictionary.
        get_cities_temperatures_report: (Generator) get the cities temperatures report.
    """
    key_to_search_for_report = 'daily'
    maximum_temperature_values_to_store = 7

    def __init__(self) -> None:
        self.cities = []

    def add_city(self, city: City) -> None:
        self.cities.append(city)
    
    def get_cities(self) -> list:
        return self.cities

    def get_cities_report_as_dict(self) -> dict:
        cities_report = {}
        for city in self.cities:
            cities_report[city.name] = city.get_temperatures_as_dict()
        return cities_report
    
    def get_cities_temperatures_report(self):
        yield "["
        for city in self.cities:
            openweathermap_response = OpenWeatherMapAPI.get_response_from_city(city)
            if openweathermap_response.status_code == OpenWeatherMapAPI.account_blocked_status_code:
                yield json.dumps({'error': 'Account blocked by openweathermap API due to exceeded the number of calls.'})
                continue

            if not openweathermap_response.status_code == OpenWeatherMapAPI.expected_status_code:
                city.set_error_report('No data provided by openweathermap api')
                continue
            
            openweathermap_response = openweathermap_response.json()
            if not openweathermap_response:
                city.set_error_report('Json from openweathermap api is empty')
                continue
            
            # check if json has valid data
            if not self.key_to_search_for_report in openweathermap_response:
                city.set_error_report('No daily data available')
                continue

            for day in openweathermap_response[self.key_to_search_for_report][:self.maximum_temperature_values_to_store]:
                temperature = TemperatureReport(
                    max_temperature=float(day['temp']['max']),
                    min_temperature=float(day['temp']['min']),
                    date=int(day['dt'])
                )
                city.add_temperature_to_report(temperature)
                
            yield json.dumps({city.name : city.get_temperatures_as_dict()})
            #yield comma if there are more cities to get if not yield nothing
            if self.cities.index(city) < len(self.cities) - 1:
                yield ","

        yield "]"
