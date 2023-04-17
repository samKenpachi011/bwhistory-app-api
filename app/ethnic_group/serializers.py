"""
Serializer for EthnicGroup Api's
"""
from rest_framework import serializers
from core.models import EthnicGroup


class EthnicGroupSerializer(serializers.ModelSerializer):
    """Serializer for the ethnic group."""
    class Meta:
        model = EthnicGroup
        fields = ['id', 'name', 'language',
                  'population', 'geography', 'history']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create ethnic group override"""

        ethinic_group = EthnicGroup.objects.create(**validated_data)

        return ethinic_group


class EthnicGroupDetailSerializer(EthnicGroupSerializer):
    """Serializer for ethnic group detail view."""

    class Meta(EthnicGroupSerializer.Meta):
        fields = EthnicGroupSerializer.Meta.fields + ['description']
