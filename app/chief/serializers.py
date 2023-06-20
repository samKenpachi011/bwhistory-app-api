"""
Serializer for Chief API's
"""
from rest_framework import serializers
from core.models import Chief


class ChiefSerializer(serializers.ModelSerializer):
    """Serializer for the chief model"""

    class Meta:
        model = Chief
        fields = ['id', 'name', 'ethnic_group']
        read_only_fields = ['id']


class ChiefDetailsSerializer(ChiefSerializer):
    """Details seriailizer for the chief model"""

    class Meta(ChiefSerializer.Meta):
        fields = ChiefSerializer.Meta.fields + ['type', 'date_of_birth', 'bio']
