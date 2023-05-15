"""
Serializer for Culture Api's
"""

from rest_framework import serializers
from core.models import Culture, EthnicGroup
from ethnic_group.serializers import EthnicGroupSerializer


class CultureSerializer(serializers.ModelSerializer):
    """Serializer for the Culture model"""
    class Meta:
        model = Culture
        fields = ['id', 'name', 'description', 'ethnic_group' ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Culture override"""
        culture = Culture.objects.create(**validated_data)

        return culture
