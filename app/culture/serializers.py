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


class CultureDetailsSerializer(CultureSerializer):
    """Serializer for culture details view"""

    class Meta(CultureSerializer.Meta):
        fields = CultureSerializer.Meta.fields + ['description']
