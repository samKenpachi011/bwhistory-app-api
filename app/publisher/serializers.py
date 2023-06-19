"""
Serializer for Publisher Api's
"""

from rest_framework import serializers
from core.models import Publisher
from django.core.files.uploadedfile import UploadedFile


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for the publisher model."""
    class Meta:
        model = Publisher
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Publisher override"""
        if self.validate_file(validated_data['document']):
            document = Publisher.objects.create(**validated_data)
            return document

    def validate_file(self, value):
        """Validate the file"""
        if not isinstance(value, UploadedFile):
            raise ValueError('Invalid file')

        max_size = 10 * 1024 * 1024  # Maximum file size (10MB)
        allowed_content_types = ['application/pdf']

        if value.size > max_size:
            raise ValueError('File too large to save')

        if value.content_type not in allowed_content_types:
            raise ValueError('Invalid file. Only PDF files are allowed.')

        return True
