"""
View for sites
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from sites import serializers
from core.models import Site


class SiteViewSet(viewsets.ModelViewSet):
    """View for managing sites"""
    serializer_class = serializers.SiteDetailsSerializer
    queryset = Site.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return site objects"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.SiteSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new site"""
        serializer.save(user=self.request.user)
