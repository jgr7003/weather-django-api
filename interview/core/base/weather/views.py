import json
import logging

from django.http import HttpResponse
from django.views import View
from django.core.cache import caches

from interview.core.base.tools.validators import validate_query_params
from interview.core.base.weather.providers import OpenWeatherMapProvider

logger = logging.getLogger(__name__)


class WeatherAPI(View):

    def get(self, request):
        validations = {}
        validate_query_params(request, validations, ["city", "country"])

        response = {}
        if len(validations) > 0:
            response["result"] = validations
            response["status_code"] = 400
        else:
            city = request.GET.get("city")
            country = request.GET.get("country")

            cache_string = "%s-%s" % (city, country)
            logger.debug("----- Search: %s", cache_string)
            cache = caches['weather'].get(cache_string)
            if cache is None:

                open_weather_provider = OpenWeatherMapProvider(city, country)
                response = open_weather_provider.search()

                if response["status_code"] == 200:
                    caches['weather'].set(cache_string, response["result"])
                    logger.debug('Set cache: %s -> %s', cache_string, response["result"])
            else:
                logger.debug('Get from cache: %s', cache_string)
                response["result"] = cache
                response["status_code"] = 200

        return HttpResponse(json.dumps(response["result"]),
                            content_type="application/json",
                            status=response["status_code"])
