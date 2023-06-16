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
    serializer_class = serializers.PublisherSerializer
    queryset = Publisher.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-id')
