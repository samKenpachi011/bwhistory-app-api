"""
View for culture information
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from culture import serializers
from core.models import Culture


class CultureViewSet(viewsets.ModelViewSet):
    """View for managing cultures"""
    serializer_class = serializers.CultureDetailsSerializer
    queryset = Culture.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve culture objects for authenticated users"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return a serializer class for the request"""
        if self.action == 'list':
            return serializers.CultureSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new culture"""
        serializer.save(user=self.request.user)
