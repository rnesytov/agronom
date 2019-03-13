from rest_framework.serializers import ModelSerializer

from .models import Field


class FieldsSerializer(ModelSerializer):
    class Meta:
        model = Field

        read_only_fields = (
            'id', 'centroid'
        )

        fields = read_only_fields + (
            'polygon', 'name', 'color', 'crop_type'
        )
