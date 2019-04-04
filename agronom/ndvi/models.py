from django.contrib.gis.db import models

from fields.models import Field


class NDVI(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, db_index=True)
    date = models.DateField()
    img = models.ImageField()
    mean = models.DecimalField(max_digits=3, decimal_places=2)
