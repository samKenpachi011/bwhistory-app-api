"""
View for publisher information
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Publisher
from publisher import serializers
from rest_framework.parsers import MultiPartParser, FormParser


class PublisherViewSet(viewsets.ModelViewSet):
    """View for managing publisher information"""

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.PublisherDetailsSerializer
    queryset = Publisher.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PublisherSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new publisher"""
        serializer.save(user=self.request.user)
