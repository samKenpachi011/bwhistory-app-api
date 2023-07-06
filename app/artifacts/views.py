"""
View for artifact information
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Artifacts
from artifacts import serializers


class ArtifactsViewSet(viewsets.ModelViewSet):
    """View for managing artifact information"""
    serializer_class = serializers.ArtifactsSerializer
    queryset = Artifacts.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns artifact objects in descending order"""
        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        """Create a new artifact"""
        if serializer.is_valid():
            serializer.save(user=self.request.user)
