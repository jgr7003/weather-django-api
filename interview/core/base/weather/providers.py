import logging

from django.conf import settings

from interview.core.base.tools.request import GETRequest
from interview.core.base.tools.xml import xml_to_dict_transform
from interview.core.base.weather.parsers import OpenWeatherMapParser

logger = logging.getLogger(__name__)


class Provider:

    def __init__(self, provider_key):
        self.provider_key = provider_key
        self.result = {}

    @property
    def provider_key(self) -> str:
        return self._provider_key

    @provider_key.setter
    def provider_key(self, value: str):
        self._provider_key = value

    def search(self) -> dict:
        raise NotImplemented


class OpenWeatherMapProvider(Provider):

    def __init__(self, city: str, country: str, lang="en"):
        super().__init__(settings.PROVIDER_OPEN_WEATHER_KEY)
        self.city = city
        self.country = country
        self.lang = lang

    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str):
        self._city = value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str):
        self._country = value

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value: str):
        self._lang = value

    def get_q(self):
        return "{city},{country}".format(
            city=self.city,
            country=self.country
        )

    def request(self, mode: str):
        url = settings.PROVIDER_OPEN_WEATHER_URL + settings.PROVIDER_OPEN_WEATHER_END_POINTS["weather"]
        query_params = {
            "q": self.get_q(),
            "appid": self.provider_key,
            "mode": mode,
            "lang": self.lang
        }
        request = GETRequest(url, query_params)
        return request.get()

    def search(self):
        response = self.request("xml")
        transform_response = xml_to_dict_transform(response.content)
        if response.status_code == 200:
            open_weather_parser = OpenWeatherMapParser(transform_response)
            result = open_weather_parser.parser()

        elif response.status_code == 404:
            result = {
                "error": transform_response["ClientError"]["message"]
            }

        else:
            raise NotImplemented

        return {
            "result": result,
            "status_code": response.status_code
        }

