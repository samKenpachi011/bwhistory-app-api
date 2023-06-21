"""
Serializer for sites app api's
"""
from rest_framework import serializers
from core.models import Site


class SiteSerializer(serializers.ModelSerializer):
    """Serializer for sites"""
    class Meta:
        model = Site
        fields = ['id', 'site_name', 'site_type']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Site override"""
        site = Site.objects.create(**validated_data)
        return site

    def update(self, instance, validated_data):
        """Update an existing Site override"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SiteDetailsSerializer(SiteSerializer):
    """Serializer for site details"""

    class Meta(SiteSerializer.Meta):
        fields = SiteSerializer.Meta.fields + [
            'culture', 'ethnic_group',
            'latitude', 'longitude',
            'importance', 'sensitivity',
            'description']
