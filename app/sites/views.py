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
    serializer_class = serializers.SiteSerializer
    queryset = Site.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return site objects"""
        return self.queryset.order_by('-id')
