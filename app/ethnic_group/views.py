"""
View for the ethnic group
"""
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        elif self.action == 'upload_image':
            return serializers.EthnicGroupImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new ethnic group."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to the ethnic group."""

        ethnic_group = self.get_object()
        serializer = self.get_serializer(ethnic_group, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
