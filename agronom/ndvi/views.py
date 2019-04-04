import coreapi
from rest_framework import generics, schemas, pagination
from rest_framework.permissions import IsAuthenticated

from .models import NDVI
from .serializers import NDVISerializer
from weather.permissions import IsFieldOwner


class NDVIView(generics.ListAPIView):
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(name='field_id', location='query', required=True),
        ]
    )
    serializer_class = NDVISerializer
    permission_classes = (IsAuthenticated, IsFieldOwner)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return NDVI.objects.filter(field_id=self.request.query_params['field_id'])
