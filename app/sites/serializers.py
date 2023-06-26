"""
Serializer for sites app api's
"""
from rest_framework import serializers
from core.models import Site, SiteImages


class SiteImagesSerializer(serializers.ModelSerializer):
    """Serializer for site images view"""
    class Meta:
        model = SiteImages
        fields = ['id', 'site', 'images']
        read_only_fields = ['id']


class SiteSerializer(serializers.ModelSerializer):
    """Serializer for sites"""
    images = SiteImagesSerializer(many=True, required=False, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Site
        fields = ['id', 'site_name', 'site_type', 'images', 'uploaded_images']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Site override"""
        images = validated_data.pop('uploaded_images', None)
        site = Site.objects.create(**validated_data)

        if images is not None:
            SiteImages.objects.bulk_create(
                [SiteImages(site=site,
                            images=image_data) for image_data in images]
            )

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
