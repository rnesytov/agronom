from django.urls import reverse
from rest_framework import status
from datetime import datetime

from weather.models import Weather
from core.tests.base_test_case import APITestCase
from .mixin import WeatherTestMixin


class TestWeatherAPI(WeatherTestMixin, APITestCase):
    def setUp(self):
        super().setUp()

        for _ in range(3):
            Weather.objects.create(
                field=self.field,
                date=datetime(2019, 3, 20),
                data={'foo': 'bar'}
            )

    def test_get_weather(self):
        response = self.api_client.get(reverse('api_weather'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'date': '2019-03-20', 'data': {'foo': 'bar'}},
            {'date': '2019-03-20', 'data': {'foo': 'bar'}},
            {'date': '2019-03-20', 'data': {'foo': 'bar'}}
        ])

    def test_pagination(self):
        response = self.api_client.get(reverse('api_weather'), {'field_id': self.field.id, 'limit': 1, 'offset': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 3,
            'next': 'http://testserver/api/v0_1/weather/?field_id=%s&limit=1&offset=2' % self.field.id,
            'previous': 'http://testserver/api/v0_1/weather/?field_id=%s&limit=1' % self.field.id,
            'results': [{'date': '2019-03-20', 'data': {'foo': 'bar'}}]
        })
