"""
Serializer for Event API's
"""
from rest_framework import serializers
from core.models import Event, EventImages


class EventImagesSerializer(serializers.ModelSerializer):
    """Serializer for event images view"""
    class Meta:
        model = EventImages
        fields = ['id', 'event', 'images']
        read_only_fields = ['id']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""
    images = EventImagesSerializer(many=True, required=False, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Event
        fields = ['id', 'name', 'images', 'uploaded_images']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Event override"""
        images = validated_data.pop('uploaded_images', None)
        event = Event.objects.create(**validated_data)

        if images is not None:
            EventImages.objects.bulk_create(
                [EventImages(event=event,
                             images=image_data) for image_data in images]
            )

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
