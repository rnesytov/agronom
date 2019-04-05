from django.contrib.gis.db import models

from cadastral.models import CadastralInfo


class Field(models.Model):
    cadastral = models.ForeignKey(CadastralInfo, on_delete=models.CASCADE)

    polygon = models.PolygonField()
    centroid = models.PointField()

    name = models.CharField(max_length=100, default='My field')
    color = models.CharField(max_length=7, default='#333777')
    crop_type = models.CharField(max_length=100, default='Wheat')
