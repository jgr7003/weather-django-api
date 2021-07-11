from django.urls import include, path

urlpatterns = [
    path('weather', include('interview.core.base.weather.urls')),
]
