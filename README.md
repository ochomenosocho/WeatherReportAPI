### Weather Report REST API for Technical interview
### By Moisés Figueroa

#### How to run it locally

1.- Clone the repository
2.- Create a python 3 virtual environment
3.- Install the requirements:
```bash
    pip3 install django
    pip3 install djangorestframework
```
4.- To run django server on localhost for development:
```bash
    python3 manage.py runserver
```

#### How to do a request to the API

For example, to get the weather forecast for the city of Monterrey, you can do the following request:
```bash
curl -X GET 'http://127.0.0.1:8000/weather_forecast?city=monterrey'
```

or you can search for the url on your browser:
```
http://127.0.0.1:8000/weather_forecast?city=monterrey
```

#### Deployed version on AWS

You can also try the deployed version on AWS, For example, to get the weather forecast for the city of Monterrey, you can do the following request:
```bash
curl -X GET 'http://52.54.123.72/weather_forecast?city=monterrey'
```

or you can search for the url on your browser:
```
http://52.54.123.72/weather_forecast?city=monterrey
```

#### Architecture design explanation

> About the framework and the architecture

The API is designed using the Django REST framework this desition was made because it is a very popular framework for building REST APIs and it is very easy to use. The API is very simple and it is not necessary to develop a complex architecture or functions from scratch.

> About the response

The decision to implement a response that is streamed as a JSON object was made because it is a very efficient way to send data to the client, this is because the client can start processing the data as soon as it starts to receive it, instead of waiting for the whole response to be received. And this tourned out to be very important during the developement of the API because the OpenWeatherMap API was taking a lot of time to respond to the requests, and also a lot of request are being made to the OpenWeatherMap API, and this number can be variable depending on the number of cities that are returnes by the Reservamos API.

> About the utils module

The utils module was created to implement the functions that are commonly used or that are used in more than one place in the API, this functions are used to make the code more readable and to avoid repeating code or to avoid large ammounts of code in the views module.

> About the models

The models are not saving any data in a database, that's why there are no heritance from the django models.Model class.

#### Notes from the developer

- The API is deployed on AWS using an EC2 instance, the operating system is Ubuntu 22.04 LTS.
- The API is running on a virtual environment using python 3.10
- The API is running on a django development server, this because it is a technical interview and it is not necessary to use a production server as apache or nginx.