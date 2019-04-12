from rest_framework import serializers

from .models import Operation


class OperationSerializer(serializers.ModelSerializer):
    field_id = serializers.IntegerField()

    class Meta:
        model = Operation
        fields = ('id', 'field_id', 'date', 'state', 'parameters', 'name')
