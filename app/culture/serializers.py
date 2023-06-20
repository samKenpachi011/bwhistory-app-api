"""
Serializer for Culture Api's
"""

from rest_framework import serializers
from core.models import Culture
from ethnic_group.serializers import TagsSerializer
from core.helpers import _get_or_create


class CultureSerializer(serializers.ModelSerializer):
    """Serializer for the Culture model"""

    # tags serializer
    tags = TagsSerializer(required=False, many=True)

    class Meta:
        model = Culture
        fields = ['id', 'name', 'ethnic_group', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Culture override"""
        tags = validated_data.pop('tags', [])
        culture = Culture.objects.create(**validated_data)
        auth_user = self.context['request'].user
        # get or create tags
        _get_or_create(auth_user, tags, culture)

        return culture

    def update(self, instance, validated_data):
        """Update culture override"""
        tags = validated_data.pop('tags', None)
        auth_user = self.context['request'].user

        if tags is not None:
            instance.tags.clear()
            _get_or_create(auth_user, tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CultureDetailsSerializer(CultureSerializer):
    """Serializer for culture details view"""

    class Meta(CultureSerializer.Meta):
        fields = CultureSerializer.Meta.fields + ['description', 'image']


class CultureImageSerializer(serializers.ModelSerializer):
    """Serializer for culture image view"""

    class Meta:
        model = Culture
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
