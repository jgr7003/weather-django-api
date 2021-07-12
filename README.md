# Installation  and run instructions

## Clone the repository

> https://github.com/jgr7003/weather-django-api.git

Switch to program folder

> cd weather-django-api/

## Subscribe in Open-weather API

Ingress in https://openweathermap.org/price#weather and get a free key for your tests

Replace your key in the Dockerfile

> ENV PROVIDER_OPEN_WEATHER_KEY <YOUR-KEY-HERE>

## Run in docker

Ensure what Docker run in your system first, next to, follow the next instructions:

### Up the docker

> docker-compose up &

The container will be downloaded and installed, once you see something like this, the process will be finished

The docker goes up the environment, swagger of project view in http://0.0.0.0:8005 or http://localhost:8005 in any navigator.

### Execute the unit tests into the docker

> docker ps

Find the image ID weather-django-api_weather, then run the command

> docker exec -it <id image> bash

This will enter the image console to execute python commands

To run the unit tests use the command

> python manage.py test

## Run in local

For this case, ensure of your system has python installed (3.7 it´s the development version)

### Create environment variable

You create environment variable: PROVIDER_OPEN_WEATHER_KEY

#### Linux or Mac

> export PROVIDER_OPEN_WEATHER_KEY="<YOUR-KEY-HERE>"

#### Windows

Follow the next instructions: https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0

### Install dependencies

Ensure of your system has pip or installing this, then, execute the command

> pip install -r requirements.txt

### Up the runserver

You will create a venv if you prefer or run the project directly in your local python

> python manage.py runserver


## Test the service

Ingress to URL and test the service

> http://0.0.0.0:8008/weather?city=Bogota&country=co