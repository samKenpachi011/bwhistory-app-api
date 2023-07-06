"""
Serializer for Artifacts
"""
from rest_framework import serializers
from core.models import Artifacts


class ArtifactsSerializer(serializers.ModelSerializer):
    """Serializer for the Artifacts model."""

    class Meta:
        model = Artifacts
        fields = ['id', 'artifact_name']
        read_only_fields = ['id']
