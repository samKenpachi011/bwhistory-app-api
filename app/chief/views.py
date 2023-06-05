"""
View for chief information
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Chief
from chief import serializers


class ChiefViewSet(viewsets.ModelViewSet):
    """View for managing chief information"""
    serializer_class = serializers.ChiefDetailsSerializer
    queryset = Chief.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns chief objects"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Returns serializer class for the request"""
        if self.action == 'list':
            return serializers.ChiefSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new chief"""
        if serializer.is_valid():
            serializer.save(user=self.request.user)
