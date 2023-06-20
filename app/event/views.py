"""
View for event information
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Event
from event import serializers
from rest_framework.parsers import MultiPartParser, FormParser


class EventViewSet(viewsets.ModelViewSet):
    """View for managing event information"""
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.EventDetailsSerializer
    queryset = Event.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve event objects for authenticated users."""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return a serializer class for the request"""
        if self.action == 'list':
            return serializers.EventSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new event"""
        if serializer.is_valid():
            serializer.save(user=self.request.user)
