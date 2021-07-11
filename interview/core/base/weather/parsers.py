from abc import ABCMeta, abstractmethod

from interview.core.base.weather.utilities import TemperatureKelvin
from interview.core.base.tools.datetime import datetime_extract_part, datetime_now


class WeatherParserInterface:
    __metaclass__ = ABCMeta

    def parse_location_name(self) -> str:
        raise NotImplemented

    def parse_temperature(self) -> str:
        raise NotImplemented

    def parse_wind(self) -> str:
        raise NotImplemented

    def parse_cloudiness(self) -> str:
        raise NotImplemented

    def parse_pressure(self) -> str:
        raise NotImplemented

    def parse_humidity(self) -> str:
        raise NotImplemented

    def parse_sunrise(self) -> str:
        raise NotImplemented

    def parse_sunset(self) -> str:
        raise NotImplemented

    def parse_geo_coordinates(self) -> str:
        raise NotImplemented

    def parse_requested_time(self) -> str:
        raise NotImplemented

    def parse_forecast(self) -> dict:
        raise NotImplemented

    @abstractmethod
    def parser(self) -> dict:
        pass


class WeatherParser(WeatherParserInterface):

    def __init__(self, origin):
        self.origin = origin

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value: dict):
        self._origin = value

    def parser(self) -> dict:
        return {
            "location_name": self.parse_location_name(),
            "temperature": self.parse_temperature(),
            "wind": self.parse_wind(),
            "cloudiness": self.parse_cloudiness(),
            "pressure": self.parse_pressure(),
            "humidity": self.parse_humidity(),
            "sunrise": self.parse_sunrise(),
            "sunset": self.parse_sunset(),
            "geo_coordinates": self.parse_geo_coordinates(),
            "requested_time": self.parse_requested_time(),
            "forecast": self.parse_forecast()
        }


class OpenWeatherMapParser(WeatherParser):

    def __init__(self, origin):
        super().__init__(origin["current"])

    def parse_location_name(self):
        # Required structure -> "Bogota, CO"
        city = self.origin.get("city", {})
        return "{city}, {country}".format(
            city=city.get("@name", ""),
            country=str(city.get("country", "")).upper()
        )

    def parse_temperature(self) -> str:
        # Required structure -> "17 °C"
        temperature = self.origin.get("temperature")
        if self.origin["temperature"]["@unit"] == "kelvin":
            kelvin = TemperatureKelvin(float(temperature.get("@value")))
            celsius = kelvin.to_celsius()
        else:
            raise NotImplemented

        return "{value} °C".format(
            value=round(celsius)
        )

    def parse_wind(self) -> str:
        # Required structure -> Gentle breeze, 3.6 m/s, west-northwest
        speed = self.origin.get("wind", {}).get("speed", {})
        direction = self.origin.get("wind", {}).get("direction", {})
        if direction is None:
            direction = {}

        return "{name}, {value} {unit}, {direction}".format(
            name=speed.get("@name", ""),
            value=speed.get("@value", ""),
            unit=speed.get("@unit", ""),
            direction=direction.get("@name", "")
        )

    def parse_cloudiness(self) -> str:
        # Required structure -> "Scattered clouds"
        clouds = self.origin.get("clouds")
        return "{name}".format(
            name=str(clouds.get("@name", "")).capitalize()
        )

    def parse_pressure(self) -> str:
        # Required structure -> "1027 hpa"
        pressure = self.origin.get("pressure")
        return "{value} {unit}".format(
            value=pressure.get("@value", ""),
            unit=pressure.get("@unit", "")
        )

    def parse_humidity(self) -> str:
        # Required structure -> "63%"
        humidity = self.origin.get("humidity")
        return "{value} {unit}".format(
            value=humidity.get("@value", ""),
            unit=humidity.get("@unit", "")
        )

    def parse_sunrise(self) -> str:
        # Required structure -> "06:07"
        sun = self.origin.get("city", {}).get("sun", {})
        return "{hour}".format(
            hour=datetime_extract_part(sun.get("@rise"), "%Y-%m-%dT%H:%M:%S", "%H:%M")
        )

    def parse_sunset(self) -> str:
        # Required structure -> "18:00"
        sun = self.origin.get("city", {}).get("sun", {})
        return "{hour}".format(
            hour=datetime_extract_part(sun.get("@set"), "%Y-%m-%dT%H:%M:%S", "%H:%M")
        )

    def parse_geo_coordinates(self) -> str:
        # Required structure -> "[4.61, -74.08]"
        coordinates = self.origin.get("city", {}).get("coord", {})
        return "[{longitude}, {latitude}]".format(
            longitude=coordinates.get("@lon", ""),
            latitude=coordinates.get("@lat", "")
        )

    def parse_requested_time(self) -> str:
        # Required structure -> "[4.61, -74.08]"
        return "{now}".format(
            now=datetime_now("%Y-%m-%d %H:%M:%S")
        )

    def parse_forecast(self) -> dict:
        # Required structure ->  {...} "it´s not clear, this is proposed"
        weather = self.origin["weather"]

        precipitation = self.origin.get("precipitation")
        if precipitation.get("@mode") != "no":
            rain = "{percentage}% {mode} {unit}".format(
                percentage=precipitation.get("@value", 0) * 100,
                mode=precipitation.get("@mode", ""),
                unit=precipitation.get("@unit", "")
            )
        else:
            rain = "no"

        return {
            "weather": "{weather}".format(
                weather=str(weather.get("@value", "")).capitalize()
            ),
            "rain": rain
        }
