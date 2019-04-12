import json
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy

from core.tests.base_test_case import APITestCase
from ndvi.models import NDVI


class TestNDVIAPI(APITestCase):
    def setUp(self):
        super().setUp()

        self.field = mommy.make('fields.Field', cadastral__user=self.user)
        self.ndvis = mommy.make(NDVI, field=self.field, _fill_optional=True, _quantity=3)

    def test_get_ndvi(self):
        response = self.api_client.get(reverse('api_ndvi'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'boundary': json.loads(self.ndvis[0].boundary.geojson),
             'date': self.ndvis[0].date.strftime('%Y-%m-%d'),
             'img': None,
             'mean': str(self.ndvis[0].mean)},
            {'boundary': json.loads(self.ndvis[1].boundary.geojson),
             'date': self.ndvis[1].date.strftime('%Y-%m-%d'),
             'img': None,
             'mean': str(self.ndvis[1].mean)},
            {'boundary': json.loads(self.ndvis[2].boundary.geojson),
             'date': self.ndvis[2].date.strftime('%Y-%m-%d'),
             'img': None,
             'mean': str(self.ndvis[2].mean)}])

    def test_pagination(self):
        response = self.api_client.get(reverse('api_ndvi'), {'field_id': self.field.id, 'limit': 1, 'offset': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 3,
            'next': 'http://testserver/api/v0_1/ndvi/?field_id=%s&limit=1&offset=2' % self.field.id,
            'previous': 'http://testserver/api/v0_1/ndvi/?field_id=%s&limit=1' % self.field.id,
            'results': [
                {'boundary': json.loads(self.ndvis[1].boundary.geojson),
                 'date': self.ndvis[1].date.strftime('%Y-%m-%d'),
                 'img': None,
                 'mean': str(self.ndvis[1].mean)}
            ]})

    def test_no_authenticated(self):
        self.api_client.logout()
        response = self.api_client.get(reverse('api_ndvi'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_invalid_field_owner(self):
        email = 'testuser@test.test'
        password = 'q123'
        self._create_user(email, password)
        self.api_client.login(email=email, password=password)
        response = self.api_client.get(reverse('api_ndvi'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})
