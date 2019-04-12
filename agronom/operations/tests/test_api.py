from rest_framework import status
from django.urls import reverse
from datetime import datetime
from model_mommy import mommy
from django.utils.timezone import get_current_timezone

from core.tests.base_test_case import APITestCase
from operations.models import Operation


class TestOperationsAPI(APITestCase):
    def setUp(self):
        super().setUp()

        date = datetime(2019, 4, 1)
        self.field = mommy.make('fields.Field', cadastral__user=self.user)
        self.operations = mommy.make(
            Operation,
            date=date,
            field=self.field,
            _fill_optional=True,
            _quantity=3)
        self.expected_date = date.astimezone(get_current_timezone()).isoformat()

    def test_get_operations(self):
        response = self.api_client.get(reverse('api_operations'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.json(), [{
            'id': self.operations[i].id,
            'date': self.expected_date,
            'field_id': self.field.id,
            'parameters': {},
            'state': self.operations[i].state,
            'name': self.operations[i].name}
            for i in range(len(self.operations))
        ])

    def test_pagination(self):
        response = self.api_client.get(reverse('api_operations'), {'field_id': self.field.id, 'limit': 1, 'offset': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 3,
            'next': 'http://testserver/api/v0_1/operations/?field_id=%s&limit=1&offset=2' % self.field.id,
            'previous': 'http://testserver/api/v0_1/operations/?field_id=%s&limit=1' % self.field.id,
            'results': [{
                'id': self.operations[1].id,
                'date': self.expected_date,
                'field_id': self.field.id,
                'parameters': {},
                'state': self.operations[1].state,
                'name': self.operations[1].name}]})

    def test_create_operation(self):
        response = self.api_client.post(
            reverse('api_operations'), {
                'field_id': self.field.id,
                'date': '2019-01-04T00:00:00',
                'state': 0,
                'parameters': {'foo': 'bar'},
                'name': 'Test operation'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        operation = Operation.objects.last()
        self.assertEqual(operation.field, self.field)
        self.assertEqual(operation.state, Operation.DONE)
        self.assertEqual(operation.parameters, {'foo': 'bar'})

    def test_no_authenticated(self):
        self.api_client.logout()
        response = self.api_client.get(reverse('api_operations'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_invalid_field_owner(self):
        email = 'testuser@test.test'
        password = 'q123'
        self._create_user(email, password)
        self.api_client.login(email=email, password=password)
        response = self.api_client.get(reverse('api_operations'), {'field_id': self.field.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_delete_operation(self):
        opertaion = mommy.make(Operation, field__cadastral__user=self.user)
        response = self.api_client.delete(reverse('api_operations'), data={'id': opertaion.id})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Operation.DoesNotExist):
            opertaion.refresh_from_db()

    def test_update_operation(self):
        operation = mommy.make(Operation, field__cadastral__user=self.user)
        response = self.api_client.put(
            reverse('api_operations'),
            data={
                'id': operation.id,
                'field_id': operation.field_id,
                'name': 'Edited name',
                'date': operation.date,
                'state': Operation.DONE,
                'parameters': {}})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        operation.refresh_from_db()
        self.assertEqual(operation.name, 'Edited name')
        self.assertEqual(operation.state, Operation.DONE)
