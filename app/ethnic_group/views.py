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

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter'
            ),
        ]
    )
)
class EthnicGroupViewSet(viewsets.ModelViewSet):
    """View for managing ethnic groups"""

    serializer_class = serializers.EthnicGroupDetailSerializer
    queryset = EthnicGroup.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string to integers"""
        return [int(x) for x in qs.split(',')]

    def get_queryset(self):
        """Retrieve ethnic group objects for authenticated users"""
        tags = self.request.query_params.get('tags')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(
            user=self.request.user
            ).order_by('-id').distinct()

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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to groups'
            ),
        ]
    )
)
class BaseAttrViewSet(mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Base viewset for ethnicgroup attributes"""
    authentication_classes = [TokenAuthentication]
    permissions_classes = [IsAuthenticated]


class TagsViewSet(BaseAttrViewSet):
    """View set for tags."""

    serializer_class = serializers.TagsSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Return tags for authenticated users."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(ethnicgroup__isnull=False)
        return queryset.order_by('-name').distinct()
