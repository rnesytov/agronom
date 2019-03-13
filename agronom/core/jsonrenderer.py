from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import renderers


class DecimalJSONRenderer(renderers.JSONRenderer):
    encoder_class = DjangoJSONEncoder
