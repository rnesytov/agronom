from django.urls import reverse
from rest_framework import status
from datetime import datetime
from model_mommy import mommy

from weather.models import Weather
from core.tests.base_test_case import APITestCase


class TestWeatherAPI(APITestCase):
    def setUp(self):
        super().setUp()

        date = datetime(2019, 4, 1)
        self.expected_date = date.strftime('%Y-%m-%d')

        self.field = mommy.make('fields.Field', cadastral__user=self.user)
        self.weathers = mommy.make(
            Weather,
            data={'foo': 'bar'},
            date=date,
            field=self.field,
            _fill_optional=True,
            _quantity=3)

    def test_get_weather(self):
        response = self.api_client.get(reverse('api_weather'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'date': self.expected_date, 'data': {'foo': 'bar'}},
            {'date': self.expected_date, 'data': {'foo': 'bar'}},
            {'date': self.expected_date, 'data': {'foo': 'bar'}}
        ])

    def test_pagination(self):
        response = self.api_client.get(reverse('api_weather'), {'field_id': self.field.id, 'limit': 1, 'offset': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 3,
            'next': 'http://testserver/api/v0_1/weather/?field_id=%s&limit=1&offset=2' % self.field.id,
            'previous': 'http://testserver/api/v0_1/weather/?field_id=%s&limit=1' % self.field.id,
            'results': [{'date': self.expected_date, 'data': {'foo': 'bar'}}]
        })

    def test_no_authenticated(self):
        self.api_client.logout()
        response = self.api_client.get(reverse('api_weather'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_invalid_field_owner(self):
        email = 'testuser@test.test'
        password = 'q123'
        self._create_user(email, password)
        self.api_client.login(email=email, password=password)
        response = self.api_client.get(reverse('api_weather'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})
