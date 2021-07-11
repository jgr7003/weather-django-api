import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from interview.core.base.weather.providers import Provider, OpenWeatherMapProvider
from interview.core.base.weather.parsers import WeatherParser, OpenWeatherMapParser


class OpenWeatherMapParserTests(TestCase):

    def setUp(self) -> None:
        self.mock = {"current": {"city": {"@id": "3688689", "@name": "Bogota", "coord": {"@lon": "-74.0817", "@lat": "4.6097"}, "country": "CO", "timezone": "-18000", "sun": {"@rise": "2021-07-11T10:50:34", "@set": "2021-07-11T23:12:44"}}, "temperature": {"@value": "291.88", "@min": "291.88", "@max": "291.88", "@unit": "kelvin"}, "feels_like": {"@value": "291.06", "@unit": "kelvin"}, "humidity": {"@value": "48", "@unit": "%"}, "pressure": {"@value": "1024", "@unit": "hPa"}, "wind": {"speed": {"@value": "1.54", "@unit": "m/s", "@name": "Calm"}, "gusts": None, "direction": {"@value": "130", "@code": "SE", "@name": "SouthEast"}}, "clouds": {"@value": "40", "@name": "scattered clouds"}, "visibility": {"@value": "10000"}, "precipitation": {"@mode": "no"}, "weather": {"@number": "802", "@value": "scattered clouds", "@icon": "03d"}, "lastupdate": {"@value": "2021-07-11T21:51:18"}}}
        self.open_weather_map = OpenWeatherMapParser(self.mock)

    def test_is_subclass(self):
        self.assertTrue(issubclass(OpenWeatherMapParser, WeatherParser))

    def test_parse_location_name(self):
        location_name = self.open_weather_map.parse_location_name()
        self.assertTrue(isinstance(location_name, str))
        self.assertEqual(location_name, "Bogota, CO")

    def test_parse_temperature(self):
        temperature = self.open_weather_map.parse_temperature()
        self.assertTrue(isinstance(temperature, str))
        self.assertEqual(temperature, "19 °C")

    def test_parse_wind(self):
        wind = self.open_weather_map.parse_wind()
        self.assertTrue(isinstance(wind, str))
        self.assertEqual(wind, "Calm, 1.54 m/s, SouthEast")

    def test_parse_cloudiness(self):
        cloudiness = self.open_weather_map.parse_cloudiness()
        self.assertTrue(isinstance(cloudiness, str))
        self.assertEqual(cloudiness, "Scattered clouds")

    def test_parse_pressure(self):
        pressure = self.open_weather_map.parse_pressure()
        self.assertTrue(isinstance(pressure, str))
        self.assertEqual(pressure, "1024 hPa")

    def test_parse_humidity(self):
        humidity = self.open_weather_map.parse_humidity()
        self.assertTrue(isinstance(humidity, str))
        self.assertEqual(humidity, "48 %")

    def test_parse_sunrise(self):
        sunrise = self.open_weather_map.parse_sunrise()
        self.assertTrue(isinstance(sunrise, str))
        self.assertEqual(sunrise, "10:50")

    def test_parse_sunset(self):
        sunset = self.open_weather_map.parse_sunset()
        self.assertTrue(isinstance(sunset, str))
        self.assertEqual(sunset, "23:12")

    def test_parse_geo_coordinates(self):
        geo_coordinates = self.open_weather_map.parse_geo_coordinates()
        self.assertTrue(isinstance(geo_coordinates, str))
        self.assertEqual(geo_coordinates, "[-74.0817, 4.6097]")

    def test_parse_requested_time(self):
        requested_time = self.open_weather_map.parse_requested_time()
        self.assertTrue(isinstance(requested_time, str))

    def test_parse_forecast(self):
        forecast = self.open_weather_map.parse_forecast()
        self.assertTrue(isinstance(forecast, dict))
        self.assertEqual(forecast["weather"], "Scattered clouds")
        self.assertEqual(forecast["rain"], "no")


class OpenWeatherMapProviderTests(TestCase):

    def test_is_subclass(self):
        self.assertTrue(issubclass(OpenWeatherMapProvider, Provider))

    def test_search(self):
        open_weather_map = OpenWeatherMapProvider("Cali", "co")
        data = open_weather_map.search()
        self.assertIn("result", data)
        self.assertIn("status_code", data)


class WeatherAPITests(APITestCase):
    def setUp(self) -> None:
        self.reverse_url = reverse('get-weather')
        print("Reverse URL -> " + self.reverse_url)

    def test_success(self):
        url = "{url}?city={city}&country={country}".format(
            url=self.reverse_url,
            city="Bogota",
            country="co"
        )
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(data["location_name"], 'Bogota, CO', response.content)
        self.assertIn("location_name", data)
        self.assertIn("temperature", data)
        self.assertIn("wind", data)
        self.assertIn("cloudiness", data)
        self.assertIn("pressure", data)
        self.assertIn("humidity", data)
        self.assertIn("sunrise", data)
        self.assertIn("sunset", data)
        self.assertIn("geo_coordinates", data)
        self.assertIn("requested_time", data)
        self.assertIn("forecast", data)

    def test_bad_requests(self):
        url = "{url}?city={city}".format(
            url=self.reverse_url,
            city="Bogota",
        )
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400, response.content)
        self.assertIn("country", data)

        url = "{url}?country={country}".format(
            url=self.reverse_url,
            country="co",
        )
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400, response.content)
        self.assertIn("city", data)

        url = "{url}?city={city}&country={country}".format(
            url=self.reverse_url,
            city="WakandaCity",
            country="co"
        )
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404, response.content)
        self.assertIn("error", data)

