from unittest.mock import patch, call
from freezegun import freeze_time
from datetime import datetime
from model_mommy import mommy

from weather.tasks import load_weather_history_for_field, update_current_weather_for_all_fields
from core.tests.base_test_case import BaseTestCase


class TestWeatherTasks(BaseTestCase):
    @patch('weather.tasks.GetWeatherHistory')
    def test_load_weather_history_for_field(self, service):
        field_id = -1

        load_weather_history_for_field(field_id)
        service().assert_called_once_with(field_id)

    @patch('weather.tasks.GetWeatherData')
    @freeze_time('2019-03-20')
    def test_update_current_weather_for_all_fields(self, service):
        fields = mommy.make('fields.Field', _fill_optional=True, _quantity=2)

        update_current_weather_for_all_fields()

        service().get.run.assert_has_calls([
            call(begin_date=datetime.now(), end_date=datetime.now(), field_id=fields[0].id),
            call(begin_date=datetime.now(), end_date=datetime.now(), field_id=fields[1].id)
        ])
