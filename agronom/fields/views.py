import coreapi
from rest_framework import generics, serializers, schemas
from rest_framework.permissions import IsAuthenticated


from .serializers import FieldsSerializer
from .services import CheckPolygon
from .models import Field
from cadastral.permissions import IsCadastralOwner
from weather.tasks import load_weather_history_for_field
from core.views import ListCreateDestroyUpdateAPIView


class FieldsView(ListCreateDestroyUpdateAPIView):
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(name='cadastral_id', location='path', required=True),
        ]
    )
    permission_classes = (IsAuthenticated, IsCadastralOwner)
    serializer_class = FieldsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        return generics.get_object_or_404(Field, id=self.request.data['id'])

    def get_queryset(self):
        return Field.objects.filter(
            cadastral_id=self.kwargs['cadastral_id']
        ).order_by('id')

    def perform_create(self, serializer):
        result = CheckPolygon().check.run(
            cadastral_id=self.kwargs['cadastral_id'],
            polygon=serializer.validated_data['polygon'],
        )

        if result.is_success:
            field = serializer.save(
                cadastral_id=self.kwargs['cadastral_id'],
                centroid=result.value
            )

            load_weather_history_for_field.delay(field.id)
        else:
            if result.failed_because(CheckPolygon().check.failures.invalid_geometry_type):
                raise serializers.ValidationError('Invalid geometry type')
