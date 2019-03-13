from celery import shared_task
from datetime import datetime

from .services import GetWeatherData, GetWeatherHistory
from fields.models import Field


@shared_task(ignore_result=True)
def load_weather_history_for_field(field_id):
    GetWeatherHistory()(field_id)


@shared_task(ignore_result=True)
def update_current_weather_for_all_fields():
    qs = Field.objects.values('id').order_by('id')

    for field_dict in qs.iterator():
        GetWeatherData().get.run(
                field_id=field_dict['id'],
                begin_date=datetime.now(),
                end_date=datetime.now()
        )
