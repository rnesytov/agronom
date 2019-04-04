from rest_framework import serializers

from .models import NDVI


class NDVISerializer(serializers.ModelSerializer):
    class Meta:
        model = NDVI
        fields = ('date', 'img', 'mean')
