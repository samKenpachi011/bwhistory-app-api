"""
Serializer for Culture Api's
"""

from rest_framework import serializers
from core.models import Culture


class CultureSerializer(serializers.ModelSerializer):
    """Serializer for the Culture model"""
    class Meta:
        model = Culture
        fields = ['id', 'name', 'ethnic_group']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Culture override"""
        culture = Culture.objects.create(**validated_data)

        return culture


class CultureDetailsSerializer(CultureSerializer):
    """Serializer for culture details view"""

    class Meta(CultureSerializer.Meta):
        fields = CultureSerializer.Meta.fields + ['description']
