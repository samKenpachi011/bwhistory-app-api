"""
View for the ethnic group
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ethnic_group import serializers
from core.models import EthnicGroup, Tag


class EthnicGroupViewSet(viewsets.ModelViewSet):
    """View for managing ethnic groups"""

    serializer_class = serializers.EthnicGroupDetailSerializer
    queryset = EthnicGroup.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve ethnic group objects for authenticated users"""

        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.EthnicGroupSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new ethnic group."""
        serializer.save(user=self.request.user)


class TagsViewSet(mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """View set for tags."""

    serializer_class = serializers.TagsSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permissions_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tags for authenticated users."""
        return self.queryset.order_by('-name')
