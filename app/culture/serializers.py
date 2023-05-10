"""
Serializer for Culture Api's
"""

from rest_framework import serializers
from core.models import Culture


class CultureSerializer(serializers.ModelSerializer):
    """Serializer for the Culture model"""

    class Meta:
        model = Culture
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
