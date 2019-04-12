from django.contrib import admin

from .models import Operation


@admin.register(Operation)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'state')
    search_fields = ('field_id',)
