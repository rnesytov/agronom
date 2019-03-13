from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin

from .models import CadastralInfo
from fields.models import Field


class FieldsInline(LeafletGeoAdminMixin, admin.TabularInline):
    model = Field
    extra = 0

    fields = ('name', 'polygon')


@admin.register(CadastralInfo)
class CadastralAdmin(LeafletGeoAdmin):
    map_height = '600px'
    search_fields = ('cadastral_number',)
    list_filter = ('loading_state', )
    list_display = ('id', 'cadastral_number', 'loading_state')

    inlines = (FieldsInline,)
