"""
Serializer for Publisher Api's
"""

from rest_framework import serializers
from core.models import Publisher
import os
from django.core.files.uploadedfile import UploadedFile


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for the publisher model."""
    class Meta:
        model = Publisher
        fields = ['id', 'document']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new Publisher override"""
        document = validated_data.pop('document', None)
        instance = Publisher.objects.create(**validated_data)
        is_validated = self.validate_file(document)
        if (type(is_validated) is not type(document)):
            raise is_validated

        instance.document = is_validated
        instance.save()
        return instance

    def validate_file(self, document):

        max_size = 10 * 1024 * 1024  # Maximum file size (10MB)
        allowed_content_types = ['application/pdf']
        allowed_extensions = ['.pdf']
        file_extension = os.path.splitext(document.name)[1]

        if not isinstance(document, UploadedFile):
            return serializers.ValidationError(
                'Invalid document. Please upload a file.')
        elif file_extension.lower() not in allowed_extensions:
            return serializers.ValidationError(
                'Invalid file extension. Only PDF files are allowed.')
        elif document.size > max_size:
            raise ValueError('File too large to save')
        elif document.content_type not in allowed_content_types:
            raise ValueError('Invalid file. Only PDF files are allowed.')

        return document


class PublisherDetailsSerializer(PublisherSerializer):
    """Serializer for publisher details view"""
    class Meta(PublisherSerializer.Meta):
        fields = PublisherSerializer.Meta.fields + ['document_type']
