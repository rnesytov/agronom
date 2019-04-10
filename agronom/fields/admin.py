from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Field


@admin.register(Field)
class FieldAdmin(LeafletGeoAdmin):
    map_height = '600px'
    search_fields = ('name',)
    list_display = ('id', 'name', 'color')
