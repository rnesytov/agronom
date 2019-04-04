from datetime import datetime

from core.tests.base_test_case import BaseTestCase
from fields.tests.helpers import setup_cadastral_info, setup_field
from ndvi.services import GetFiledProducts, LoadNDVI
from fields.models import Field


class TestGetProductsForFields(BaseTestCase):
    def test_load(self):
        cad = setup_cadastral_info(self.user)
        field = setup_field(cad)

        result = GetFiledProducts()(Field.objects.filter(id=field.id), datetime.now())

        for k, v in result.items():
            LoadNDVI().load(k, v, False)

    # def test_one_more(self):
    #     cad = setup_cadastral_info(self.user)
    #     field = setup_field(cad)
