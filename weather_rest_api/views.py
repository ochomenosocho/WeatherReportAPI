from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


from .models import City, WeatherReport, TemperatureReport

#import API classes from utils
from .utils.apis import OpenWeatherMapAPI, ReservamosAPI
from .utils.parameter import is_valid_parameter, is_valid_city_element

# Create your views here.
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def weather_forecast(request):
    city_name = request.GET.get('city', '')

    #check if parameter is valid
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

    # get the lat and lon from the response
    weather_report = WeatherReport()
 
    for element in reservamos_response:
        if not is_valid_city_element(element):
            continue
        city = City(
                name=element['city_name'],
                latitude=float(element['lat']),
                longitude=float(element['long'])
            )
        weather_report.add_city(city)
    
    #check if there are cities to get weather report
    if not weather_report.get_cities():
        return Response({ 'error': 'No cities to get weather report' }, status=404) # not found 

    for city in weather_report.get_cities():
        openweathermap_response = OpenWeatherMapAPI.get_response_from_city(city)
        if openweathermap_response.status_code == OpenWeatherMapAPI.account_blocked_status_code:
            return Response({ 'error': 'Account blocked by openweathermap API due to excedded the number of calls.' }, status=openweathermap_response.status_code)

        if not openweathermap_response.status_code == OpenWeatherMapAPI.expected_status_code:
            city.set_error_report('No data provided by openweathermap api')
        
        openweathermap_response = openweathermap_response.json()
        if not openweathermap_response:
            city.set_error_report('Json from openweathermap api is empty')
        
        # check if json has valid data
        if not weather_report.key_to_search_for_report in openweathermap_response:
            # handle the case where 'daily' is not present in the response
            city.set_error_report('No daily data available')

        for day in openweathermap_response[weather_report.key_to_search_for_report][:weather_report.maximum_temperature_values_to_store]:
            temperature = TemperatureReport(
                max_temperature=float(day['temp']['max']),
                min_temperature=float(day['temp']['min']),
                date=int(day['dt'])
            )
            city.add_temperature_to_report(temperature)

    return Response(weather_report.get_cities_report_as_dict(), status=status.HTTP_200_OK)