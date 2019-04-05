from datetime import timedelta, date
from django.conf import settings

from .mixins import SentinelAPIMixin
from ndvi.models import NDVI


class GetFieldProducts(SentinelAPIMixin):
    API_PLATFORM_NAME = 'Sentinel-2'
    API_PRODUCT_TYPE = 'S2MSI1C'

    def __init__(self):
        self.api = self.get_api()

    @property
    def days_past(self):
        return timedelta(settings.SENTINEL_PRODUCTS_DAYS_PAST)

    @property
    def max_clouds_percentage(self):
        return settings.SENTINEL_MAX_CLOUD_PERCENTAGE

    def get_product_ids(self, area, product_date):
        products = self.api.query(
            area=area,
            area_relation='Contains',
            date=(product_date - self.days_past, product_date),
            platformname=self.API_PLATFORM_NAME,
            producttype=self.API_PRODUCT_TYPE,
            cloudcoverpercentage=(0, self.max_clouds_percentage)
        )

        date_id_dict = {}

        for k, v in products.items():
            date_id_dict[v['beginposition']] = k

        return date_id_dict.values()

    def _filter_same_date(self, products):
        res = {}
        for k, v in products.items():
            res

    def __call__(self, fields_qs, product_date=None):
        if product_date is None:
            product_date = date.today()

        product_fields_map = {}

        for field in fields_qs.iterator():
            products_ids = set(self.get_product_ids(field.polygon.wkt, product_date))

            existing = set(
                NDVI.objects.filter(
                    field=field,
                    product_id__in=products_ids
                ).values_list('product_id', flat=True)
            )

            for product_id in products_ids - existing:
                product_fields_map[product_id] = product_fields_map.get(product_id, []) + [field.id]

        return product_fields_map
