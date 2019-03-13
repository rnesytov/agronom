from rest_framework import serializers

from .models import CadastralInfo


class CadastralListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralInfo

        read_only_fields = (
            'id', 'loading_state'
        )
        fields = read_only_fields + (
            'cadastral_number',
        )


class CadastralRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralInfo

        read_only_fields = (
            'id', 'loading_state', 'cadastral_number', 'polygon'
        )
        fields = read_only_fields
