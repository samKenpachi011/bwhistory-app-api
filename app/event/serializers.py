"""
Serializer for Event API's
"""
from rest_framework import serializers
from core.models import Event, EventImages


class EventImageSerializer(serializers.ModelSerializer):
    """Serializer for EventImage models"""
    class Meta:
        model = EventImages
        fields = ['id', 'event', 'images']
        read_only_fields = ['id']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""
    class Meta:
        model = Event
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Event override"""
        event = Event.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        """Update event override"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class EventDetailsSerializer(EventSerializer):
    """Serializer for Event details view"""
    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ['description']
