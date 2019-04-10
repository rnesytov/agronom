from celery import shared_task

from fields.models import Field
from .services import GetFieldProducts, LoadNDVI


@shared_task(ignore_result=True)
def load_ndvi(product_id, field_ids):
    LoadNDVI().load.run(
        product_id=product_id,
        field_ids=field_ids,
        cleanup=True)


@shared_task(ignore_result=True)
def load_ndvi_for_field_qs(field_qs):
    for product_id, field_ids in GetFieldProducts()(field_qs).items():
        load_ndvi.delay(product_id, field_ids)


@shared_task(ignore_result=True)
def load_ndvi_for_all_fields():
    field_qs = Field.objects.all().order_by('id')

    load_ndvi_for_field_qs(field_qs)
