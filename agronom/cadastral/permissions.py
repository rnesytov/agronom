from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .models import CadastralInfo


class IsCadastralOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

    def has_permission(self, request, view):
        cad_info = get_object_or_404(CadastralInfo, id=view.kwargs['cadastral_id'])

        return cad_info.user == request.user
