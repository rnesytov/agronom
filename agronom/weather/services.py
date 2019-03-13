import requests
from enum import Enum, auto
from datetime import datetime, timedelta
from stories import story, arguments, Success, Failure, Result
from stories.shortcuts import failures_in
from django.conf import settings

from fields.models import Field
from .models import Weather


class GetWeatherData:
    API_URL = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'
    API_DATE_FORMAT = '%Y-%m-%d'

    @story
    @arguments('field_id', 'begin_date', 'end_date')
    def get(I):
        I.find_field_obj
        I.send_api_request
        I.check_api_response
        I.save_obj

    def set_date(self, ctx):
        return Success(
            begin_date=datetime.now(),
            end_date=datetime.now() - timedelta(settings.WEATHER_HISTORY_DAYS)
        )

    def find_field_obj(self, ctx):
        field = Field.objects.get(id=ctx.field_id)

        return Success(field=field)

    def send_api_request(self, ctx):
        try:
            response = requests.get(
                self.API_URL,
                params={
                    'q': '%s,%s' % (ctx.field.centroid.x, ctx.field.centroid.y),
                    'date': ctx.begin_date.strftime(self.API_DATE_FORMAT),
                    'enddate': ctx.end_date.strftime(self.API_DATE_FORMAT),
                    'tp': 24,
                    'format': 'json',
                    'key': settings.WEATHER_API_KEY
                },
                timeout=settings.WEATHER_API_TIMEOUT
            )

            return Success(response=response)
        except requests.exceptions.Timeout:
            return Failure(Errors.api_timeout)

    def check_api_response(self, ctx):
        response = ctx.response

        if response.status_code == requests.codes.ok:
            json = response.json()

            if json.get('data') is not None and json.get('data').get('weather') is not None:
                return Success(weather_data=json['data']['weather'])

        return Failure(Errors.invalid_api_response)

    def save_obj(self, ctx):
        def create_weather_obj(weather_data):
            date = datetime.strptime(weather_data['date'], self.API_DATE_FORMAT).date()

            return Weather(
                field=ctx.field,
                date=date,
                data=weather_data
            )

        weather_objects = list(map(create_weather_obj, ctx.weather_data))
        Weather.objects.bulk_create(weather_objects)

        return Result()


class GetWeatherHistory:
    @property
    def bulk_days(self):
        return timedelta(settings.WEATHER_HISTORY_DAYS_IN_BULK)

    def calc_periods(self, begin_date):
        bulk_number = 1
        current = begin_date

        while bulk_number <= settings.WEATHER_HISTORY_COUNT_BULKS:
            yield (current - self.bulk_days, current)

            current -= self.bulk_days + timedelta(1)
            bulk_number += 1

    def __call__(self, field_id, end_date=None):
        if end_date is None:
            end_date = datetime.now()

        for period in self.calc_periods(end_date):
            GetWeatherData().get.run(field_id, period[0], period[1])


@failures_in(GetWeatherData)
class Errors(Enum):
    api_timeout = auto()
    invalid_api_response = auto()
