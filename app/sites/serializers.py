"""
Serializer for sites app api's
"""
from rest_framework import serializers
from core.models import Site


class SiteSerializer(serializers.ModelSerializer):
    """Serializer for sites"""
    class Meta:
        model = Site
        fields = ['id', 'site_name']
        read_only_fields = ['id']
