import coreapi
from rest_framework import generics, schemas, pagination
from rest_framework.permissions import IsAuthenticated

from .models import Weather
from .serializers import WeatherSerializer
from .permissions import IsFieldOwner


class WeatherView(generics.ListAPIView):
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(name='field_id', location='query', required=True),
        ]
    )
    serializer_class = WeatherSerializer
    permission_classes = (IsAuthenticated, IsFieldOwner)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return Weather.objects.filter(field_id=self.request.query_params['field_id'])
