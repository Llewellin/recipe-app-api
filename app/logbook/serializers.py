from rest_framework import serializers

from core.models import Wonder


class WonderSerializer(serializers.ModelSerializer):
    """Serializer for Wonder Object"""

    class Meta:
        model = Wonder
        fields = ('id', 'name', 'category')
        read_only_field = ('id',)
