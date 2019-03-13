import responses
import json
import os
import freezegun
from datetime import datetime
from unittest.mock import patch, call

from weather.services import GetWeatherData, GetWeatherHistory
from core.tests.base_test_case import BaseTestCase
from .mixin import WeatherTestMixin


class TestGetWeather(WeatherTestMixin, BaseTestCase):
    WEATHER_BEGIN_DATE = datetime(2019, 3, 17)
    WEATHER_END_DATE = datetime(2019, 3, 20)

    @staticmethod
    def load_fixture(name, mode='r'):
        script_dir = os.path.dirname(__file__)
        fixture_path = os.path.join(script_dir, 'fixtures', name)

        with open(fixture_path, mode) as f:
            return f.read()

    @responses.activate
    def test_get_weather_for_field(self):
        response_fixture = self.load_fixture('weather_api_response.json')
        responses.add(
            responses.GET,
            GetWeatherData.API_URL,
            body=response_fixture,
            status=200
        )
        result = GetWeatherData().get.run(self.field.id, self.WEATHER_BEGIN_DATE, self.WEATHER_END_DATE)

        self.assertTrue(result.is_success)
        self.assertEqual(responses.calls[0].request.path_url, (
            '/premium/v1/past-weather.ashx?q=38.20744514465332%2C53.9711579991986&date=2019-03-17&enddate=2019-03-20'
            '&tp=24&format=json&key=570cabc13dca49dab1295355190104'
            ))

        weather_data = json.loads(response_fixture)['data']['weather']
        for idx, w in enumerate(self.field.weather_set.order_by('date')):
            self.assertEquals(w.date.strftime('%Y-%m-%d'), weather_data[idx]['date'])
            self.assertEquals(w.data, weather_data[idx])

    @responses.activate
    def test_invalid_api_response(self):
        responses.add(
            responses.GET,
            GetWeatherData.API_URL,
            body='Internal server error',
            status=500
        )
        result = GetWeatherData().get.run(self.field.id, self.WEATHER_BEGIN_DATE, self.WEATHER_END_DATE)

        self.assertTrue(result.is_failure)
        self.assertTrue(result.failed_on('check_api_response'))
        self.assertTrue(result.failed_because(GetWeatherData().get.failures.invalid_api_response))


class TestGetWeatherHistory(WeatherTestMixin, BaseTestCase):
    @freezegun.freeze_time('2019-03-20')
    @patch('weather.services.GetWeatherData')
    def test_calc_weather_periods(self, get_weather_data):
        field_id = -1
        with self.settings(WEATHER_HISTORY_DAYS_IN_BULK=10, WEATHER_HISTORY_COUNT_BULKS=3):
            GetWeatherHistory()(field_id)

        get_weather_data().get.run.assert_has_calls([
            call(field_id, datetime(2019, 3, 10), datetime(2019, 3, 20)),
            call(field_id, datetime(2019, 2, 27), datetime(2019, 3, 9)),
            call(field_id, datetime(2019, 2, 16), datetime(2019, 2, 26))
        ])
