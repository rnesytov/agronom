from unittest.mock import patch

from ndvi.tasks import load_ndvi, load_ndvi_for_field_qs, load_ndvi_for_all_fields
from core.tests.base_test_case import BaseTestCase


class TestNDVITasks(BaseTestCase):
    @patch('ndvi.tasks.LoadNDVI')
    def test_load_ndvi(self, service):
        product_id = '-1'
        field_ids = [-1]

        load_ndvi(product_id, field_ids)

        service().load.run.assert_called_once_with(
            product_id=product_id,
            field_ids=field_ids,
            cleanup=True)

    @patch('ndvi.tasks.load_ndvi')
    @patch('ndvi.tasks.GetFieldProducts')
    def test_load_ndvi_for_fields_qs(self, service, task):
        product_id = '-1'
        field_ids = [-1]
        service().return_value = {product_id: field_ids}
        query_set = object()

        load_ndvi_for_field_qs(query_set)

        service().assert_called_once_with(query_set)
        task.delay.assert_called_once_with(product_id, field_ids)

    @patch('ndvi.tasks.Field')
    @patch('ndvi.tasks.load_ndvi_for_field_qs')
    def test_load_ndvi_for_all_fields(self, task, model):
        load_ndvi_for_all_fields()

        model.objects.all().order_by.assert_called_once_with('id')
        task.assert_called_once_with(model.objects.all().order_by())
