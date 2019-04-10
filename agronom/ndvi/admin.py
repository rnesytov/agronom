from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import NDVI


@admin.register(NDVI)
class NDVIAdmin(LeafletGeoAdmin):
    list_display = ('id', 'field_id', 'product_id', 'mean')
    search_fields = ('field_id', 'product_id')
