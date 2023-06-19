"""
Serializer for Publisher Api's
"""

from rest_framework import serializers
from core.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for the publisher model."""
    class Meta:
        model = Publisher
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Publisher override"""
        document = Publisher.objects.create(**validated_data)
        return document
