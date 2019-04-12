from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .models import Field


class IsFieldOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'POST', 'PUT'):
            field_id = request.query_params.get('field_id') or request.data['field_id']
            field = get_object_or_404(Field, pk=field_id)

            return field.cadastral.user == request.user
        else:
            return True
