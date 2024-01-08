from datetime import datetime

# Create your models here.
class TemperatureReport():
    """
    Class to manage the temperature report of each city.

    attributes:
        max_temperature: maximum temperature.
        min_temperature: minimum temperature.
        date: date of the temperature.
    
    methods:
        get_temperatures_as_dict: get the temperatures ordered by date as dictionary.
    """
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
    """
    Class to manage the cities.

    Attributes:
        name: name of the city.
        latitude: latitude of the city.
        longitude: longitude of the city.
        temperatures: temperatures of the city.
        error_report: error report of the city.

    Methods:
        set_error_report: set the error report of the city.
        add_temperature_to_report: add temperature to the city.
        get_temperatures_as_dict: get temperature elements as dictionary.
    """
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