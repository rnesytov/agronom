from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Field
from weather.models import Weather


class WeatherInline(admin.TabularInline):
    model = Weather
    extra = 0


@admin.register(Field)
class FieldAdmin(LeafletGeoAdmin):
    map_height = '600px'
    search_fields = ('name',)
    list_display = ('id', 'name')

    inlines = (WeatherInline,)
