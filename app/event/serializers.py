"""
Serializer for Event API's
"""
from rest_framework import serializers
from core.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""

    class Meta:
        model = Event
        fields = ['id', 'name']
        read_only_fields = ['id']
