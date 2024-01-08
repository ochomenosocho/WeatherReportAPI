from django.http import StreamingHttpResponse

# import rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

# import models
from .models import City

#import resources
from .utils.apis import ReservamosAPI
from .utils.parameter import is_valid_parameter, is_valid_city_element
from .utils.WeatherReport import WeatherReport

# Create your views here.
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def weather_forecast(request):
    """
    View to get the temperature weather forecast of the next 7 days for the city provided by the user.
    
    Arguments:
        city: the city parameter to be provided by the user.
    Returns:
        A json with the temperature weather forecast of the next 7 days for the city provided by the user.
    """
    city_name = request.GET.get('city', '')

    #check if the parameter provided by user is valid
    if not is_valid_parameter(city_name):
        return Response({ 'error': 'Invalid parameter' }, status=400) # bad request

    # create a request from api: https://search.reservamos.mx/api/v2/places?q=
    reservamos_response = ReservamosAPI.get_response_from_city_name(city_name)
    if not reservamos_response.status_code == ReservamosAPI.expected_status_code:
        return Response({ 'error': 'No data provided by Reservamos api' }, status=reservamos_response.status_code)

    reservamos_response = reservamos_response.json()
    #make sure response_city has valid values
    if not reservamos_response:
        return Response({ 'error': 'No Json response from Reservamos API' }, status=400) # bad request

    weather_report = WeatherReport()
    # get the cities from the response
    for element in reservamos_response:
        if not is_valid_city_element(element):
            continue
        city = City(
                name=element['ascii_display'],
                latitude=float(element['lat']),
                longitude=float(element['long'])
            )
        weather_report.add_city(city)
    
    #check if there are cities to get weather report
    if not weather_report.get_cities():
        return Response({ 'error': 'No cities to get weather report' }, status=404) # not found

    return StreamingHttpResponse(weather_report.get_cities_temperatures_report(),status=status.HTTP_200_OK, content_type='application/json')