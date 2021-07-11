from django.urls import path

from interview.core.base.weather.views import WeatherAPI

urlpatterns = [
    path('', WeatherAPI.as_view(), name="get-weather"),
]
