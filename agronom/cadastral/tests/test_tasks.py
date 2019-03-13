from celery.exceptions import Retry
from unittest.mock import patch
from unittest import TestCase

from cadastral.services import SaveCadastralPolygon
from cadastral.tasks import get_cadastral_polygon


class TestGetCadastralPolygonTask(TestCase):
    @patch('cadastral.tasks.SaveCadastralPolygon.save_polygon')
    def test_successful_call(self, save_polygon):
        save_polygon.run().is_failure = False
        save_polygon.run.reset_mock()

        get_cadastral_polygon(42)

        save_polygon.run.assert_called_once_with(42)

    @patch('cadastral.tasks.SaveCadastralPolygon.save_polygon')
    @patch('cadastral.tasks.get_cadastral_polygon.retry')
    def test_retry(self, retry, save_polygon):
        save_polygon.run().is_failure = True
        save_polygon.run().failed_because.return_value = SaveCadastralPolygon.save_polygon.failures.api_timeout
        retry.side_effect = Retry()

        with self.assertRaises(Retry):
            get_cadastral_polygon(42)
