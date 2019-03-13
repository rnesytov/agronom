from rest_framework import permissions
from django.shortcuts import get_object_or_404

from cadastral.models import CadastralInfo


class IsCadastralOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        cad = get_object_or_404(CadastralInfo, pk=view.kwargs['cadastral_id'])

        return cad.user == request.user
