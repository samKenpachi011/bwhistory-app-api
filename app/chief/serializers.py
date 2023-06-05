"""
Serializer for Chief API's
"""
from rest_framework import serializers
from core.models import Chief


class ChiefSerializer(serializers.ModelSerializer):
    """Serializer for chief model"""

    class Meta:
        model = Chief
        fields = ['id', 'name']
        read_only_fields = ['id']
