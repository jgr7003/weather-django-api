from django.test import TestCase
from django.conf import settings

from interview.core.base.tools.datetime import *
from interview.core.base.tools.xml import *
from interview.core.base.tools.request import GETRequest


class DatetimeTests(TestCase):

    def test_extract_hour_minute(self):
        part = datetime_extract_part("2021-07-11T11:02:15", "%Y-%m-%dT%H:%M:%S", "%H:%M")
        self.assertEqual(part, "11:02")

    def test_datetime_now(self):
        now = datetime_now("%Y-%m-%d %H:%M:%S")
        self.assertTrue(isinstance(now, str))


class RequestTests(TestCase):

    def test_request_get(self):
        url = settings.PROVIDER_OPEN_WEATHER_URL + settings.PROVIDER_OPEN_WEATHER_END_POINTS["weather"]
        query_params = {
            "q": "Bogota, co",
            "appid": settings.PROVIDER_OPEN_WEATHER_KEY,
            "mode": "xml"
        }
        request = GETRequest(url, query_params)
        response = request.get()
        self.assertGreater(len(response.content), 0)


class XMLTests(TestCase):

    def setUp(self) -> None:
        self.xml = '<?xml version="1.0" encoding="UTF-8"?>\n<current><city id="3687238" name="Cartagena"><coord lon="-75.5144" lat="10.3997"></coord><country>CO</country><timezone>-18000</timezone><sun rise="2021-07-11T10:46:41" set="2021-07-11T23:28:05"></sun></city><temperature value="302.94" min="302.94" max="302.94" unit="kelvin"></temperature><feels_like value="309.91" unit="kelvin"></feels_like><humidity value="79" unit="%"></humidity><pressure value="1008" unit="hPa"></pressure><wind><speed value="4.12" unit="m/s" name="Gentle Breeze"></speed><gusts></gusts><direction value="30" code="NNE" name="North-northeast"></direction></wind><clouds value="40" name="scattered clouds"></clouds><visibility value="10000"></visibility><precipitation mode="no"></precipitation><weather number="802" value="scattered clouds" icon="03d"></weather><lastupdate value="2021-07-11T22:25:07"></lastupdate></current>'

    def test_xml_to_dict_transform(self):
        transform = xml_to_dict_transform(self.xml)
        json_expended = {"current": {
            "city": {"@id": "3687238", "@name": "Cartagena", "coord": {"@lon": "-75.5144", "@lat": "10.3997"},
                     "country": "CO", "timezone": "-18000",
                     "sun": {"@rise": "2021-07-11T10:46:41", "@set": "2021-07-11T23:28:05"}},
            "temperature": {"@value": "302.94", "@min": "302.94", "@max": "302.94", "@unit": "kelvin"},
            "feels_like": {"@value": "309.91", "@unit": "kelvin"}, "humidity": {"@value": "79", "@unit": "%"},
            "pressure": {"@value": "1008", "@unit": "hPa"},
            "wind": {"speed": {"@value": "4.12", "@unit": "m/s", "@name": "Gentle Breeze"}, "gusts": None,
                     "direction": {"@value": "30", "@code": "NNE", "@name": "North-northeast"}},
            "clouds": {"@value": "40", "@name": "scattered clouds"}, "visibility": {"@value": "10000"},
            "precipitation": {"@mode": "no"},
            "weather": {"@number": "802", "@value": "scattered clouds", "@icon": "03d"},
            "lastupdate": {"@value": "2021-07-11T22:25:07"}}}

        self.assertTrue(isinstance(transform, dict))
        self.assertEqual(transform, json_expended)
