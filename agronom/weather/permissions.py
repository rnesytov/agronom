from rest_framework import permissions
from django.shortcuts import get_object_or_404

from fields.models import Field


class IsFieldOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        field = get_object_or_404(Field, pk=request.query_params['field_id'])

        return field.cadastral.user == request.user
