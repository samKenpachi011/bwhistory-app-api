"""
View for culture information
"""
from rest_framework import (
    viewsets,
    status)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from culture import serializers
from core.models import Culture, Tag
from core.helpers import _params_to_ints
from ethnic_group.views import BaseAttrViewSet
from ethnic_group.serializers import TagsSerializer

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
class CultureViewSet(viewsets.ModelViewSet):
    """View for managing cultures"""
    serializer_class = serializers.CultureDetailsSerializer
    queryset = Culture.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve culture objects for authenticated users"""

        # filter by tags
        tags = self.request.query_params.get('tags')
        queryset = self.queryset

        if tags:
            # get tag ids
            tag_ids = _params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.order_by('-id')

    def get_serializer_class(self):
        """Return a serializer class for the request"""
        if self.action == 'list':
            return serializers.CultureSerializer
        elif self.action == 'upload_image':
            return serializers.CultureImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new culture"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload a new image to a culture."""
        culture = self.get_object()
        serializer = self.get_serializer(culture, data=request.data)

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
                description='Filter by items assigned to culture'
            ),
        ]
    )
)
class TagsViewSet(BaseAttrViewSet):
    """View set for tags"""
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Returns tags for authenticated users"""

        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )

        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(culture__isnull=False)
        return queryset.order_by('-name').distinct()
