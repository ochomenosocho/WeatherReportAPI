from datetime import datetime

# Create your models here.
class TemperatureReport():
    def __init__(self, max_temperature: float, min_temperature: float, date: int) -> None:
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature    
        self.date = datetime.strftime(datetime.fromtimestamp(date), '%Y-%m-%d')

    def get_temperatures_as_dict(self) -> dict:
        return {
            self.date : {
                'max': self.max_temperature,
                'min': self.min_temperature,
            }
        }

class City():
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.temperatures = []
        self.error_report = None

    def set_error_report(self, error_report: str) -> None:
        self.error_report = error_report
    
    #add temperature to city
    def add_temperature_to_report(self, temperature: TemperatureReport) -> None:
        self.temperatures.append(temperature)
    
    #get temperature elements as dictionary
    def get_temperatures_as_dict(self) -> dict:
        if self.error_report:
            return { 'error': self.error_report }
        temp = {}
        for temperature in self.temperatures:
            temp.update(temperature.get_temperatures_as_dict())
        return temp

class WeatherReport():
    def __init__(self) -> None:
        self.cities = []

    key_to_search_for_report = 'daily'
    maximum_temperature_values_to_store = 7

    def add_city(self, city: City) -> None:
        self.cities.append(city)
    
    def get_cities(self) -> list:
        return self.cities

    def get_cities_report_as_dict(self) -> dict:
        cities_report = {}
        for city in self.cities:
            cities_report[city.name] = city.get_temperatures_as_dict()
        return cities_report
