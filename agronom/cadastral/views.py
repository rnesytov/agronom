from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import CadastralInfo
from .serializers import CadastralListCreateSerializer, CadastralRetrieveSerializer
from .tasks import get_cadastral_polygon
from .permissions import IsCadastralOwner


class CadastralListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CadastralListCreateSerializer

    def get_queryset(self):
        return CadastralInfo.objects.filter(
            user_id=self.request.user.id,
        )

    def perform_create(self, serializer):
        cadastral_info = serializer.save(user=self.request.user)

        get_cadastral_polygon.delay(cadastral_info.pk)


class CadastralRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsCadastralOwner)
    serializer_class = CadastralRetrieveSerializer

    def get_object(self):
        return get_object_or_404(CadastralInfo, pk=self.kwargs['cadastral_id'])
