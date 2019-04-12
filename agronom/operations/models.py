from django.db import models
from django.contrib.postgres.fields import JSONField

from fields.models import Field


class Operation(models.Model):
    DONE = 0
    NOT_DONE = 1
    STATES = (
        (DONE, 'done'),
        (NOT_DONE, 'not done'),
    )

    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    state = models.PositiveSmallIntegerField(choices=STATES)
    parameters = JSONField()
