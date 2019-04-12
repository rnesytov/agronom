import inspect
import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    USER_EMAIL = 'test_user@takewing.ru'
    USER_PASSWORD = 'q123'

    @staticmethod
    def _create_user(email, password):
        UserModel = get_user_model()

        user = UserModel(email=email)
        user.set_password(password)
        user.save()

        return user

    def setUp(self):
        self.user = self._create_user(self.USER_EMAIL, self.USER_PASSWORD)

    def load_fixture(self, fixture_name, mode='r'):
        frame = inspect.stack()[1]
        script_dir = os.path.dirname(frame.filename)
        fixture_path = os.path.join(script_dir, 'fixtures', fixture_name)

        with open(fixture_path, mode) as f:
            return f.read()


class APITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.api_client = APIClient()
        self.api_client.login(email=self.USER_EMAIL, password=self.USER_PASSWORD)
