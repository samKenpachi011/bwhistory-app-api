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

    def create(self, validated_data):
        """Create ethnic group override"""
        tags = validated_data.pop('tags', [])
        ethinic_group = EthnicGroup.objects.create(**validated_data)
        auth_user = self.context['request'].user

        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,)

            ethinic_group.tags.add(tag_object)

        return ethinic_group


class EthnicGroupDetailSerializer(EthnicGroupSerializer):
    """Serializer for ethnic group detail view."""

    class Meta(EthnicGroupSerializer.Meta):
        fields = EthnicGroupSerializer.Meta.fields + ['description']
