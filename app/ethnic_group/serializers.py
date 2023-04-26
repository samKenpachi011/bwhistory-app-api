"""
Serializer for EthnicGroup Api's
"""
from rest_framework import serializers
from core.models import EthnicGroup, Tag


class TagsSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class EthnicGroupSerializer(serializers.ModelSerializer):
    """Serializer for the ethnic group."""
    tags = TagsSerializer(required=False, many=True)

    class Meta:
        model = EthnicGroup
        fields = ['id', 'name', 'language',
                  'population', 'geography', 'history',
                  'tags']
        read_only_fields = ['id']

    def _get_or_create(self, tags, ethnic_group):
        """Get or create a new tag."""
        auth_user = self.context['request'].user

        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,)

            ethnic_group.tags.add(tag_object)

        return ethnic_group

    def create(self, validated_data):
        """Create ethnic group override"""
        tags = validated_data.pop('tags', [])
        ethnic_group = EthnicGroup.objects.create(**validated_data)
        self._get_or_create(tags, ethnic_group)

        return ethnic_group

    def update(self, instance, validated_data):
        """Update ethnic group override"""
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class EthnicGroupDetailSerializer(EthnicGroupSerializer):
    """Serializer for ethnic group detail view."""

    class Meta(EthnicGroupSerializer.Meta):
        fields = EthnicGroupSerializer.Meta.fields + ['description']
