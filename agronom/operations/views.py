import coreapi
from rest_framework import schemas, pagination, generics
from rest_framework.permissions import IsAuthenticated

from .models import Operation
from .serializers import OperationSerializer
from fields.permissions import IsFieldOwner
from core.views import ListCreateDestroyUpdateAPIView


class OperationsView(ListCreateDestroyUpdateAPIView):
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(name='field_id', location='query', required=True),
        ]
    )
    serializer_class = OperationSerializer
    permission_classes = (IsAuthenticated, IsFieldOwner)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return Operation.objects.filter(field_id=self.request.query_params['field_id']).order_by('-date')

    def get_object(self):
        return generics.get_object_or_404(Operation, id=self.request.data['id'])
