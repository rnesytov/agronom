from unittest.mock import patch, call
from freezegun import freeze_time
from datetime import datetime

from weather.tasks import load_weather_history_for_field, update_current_weather_for_all_fields
from fields.tests.helpers import setup_field
from core.tests.base_test_case import BaseTestCase
from .mixin import WeatherTestMixin


class TestWeatherTasks(WeatherTestMixin, BaseTestCase):
    @patch('weather.tasks.GetWeatherHistory')
    def test_load_weather_history_for_field(self, service):
        field_id = -1

        load_weather_history_for_field(field_id)
        service().assert_called_once_with(field_id)

    @patch('weather.tasks.GetWeatherData')
    @freeze_time('2019-03-20')
    def test_update_current_weather_for_all_fields(self, service):
        other_field = setup_field(self.cad_info)

        update_current_weather_for_all_fields()

        service().get.run.assert_has_calls([
            call(begin_date=datetime.now(), end_date=datetime.now(), field_id=self.field.id),
            call(begin_date=datetime.now(), end_date=datetime.now(), field_id=other_field.id)
        ])
