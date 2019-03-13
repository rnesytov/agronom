from django.db import models
from django.contrib.postgres.fields import JSONField


from fields.models import Field


class Weather(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    date = models.DateField()
    data = JSONField()

    class Meta:
        ordering = ('-date',)
