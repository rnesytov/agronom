from django.contrib.gis.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class CadastralInfo(models.Model):
    NOT_LOADED = 0
    LOADED = 1
    FAILED = 2
    LOADING_STATES = (
        (NOT_LOADED, 'not loaded'),
        (LOADED, 'loaded'),
        (FAILED, 'failed')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cadastral_number = models.CharField(
        max_length=25,
        validators=[RegexValidator('[0-9]{2}:[0-9]{2}:[0-9]{1,7}:[0-9]{1,10}', 'Invalid cadastral number')]
    )
    loading_state = models.PositiveSmallIntegerField(choices=LOADING_STATES, default=NOT_LOADED)
    polygon = models.MultiPolygonField(null=True)

    def __str__(self):
        return "%s %s" % (self.__class__.__name__, self.cadastral_number)
