"""
View for event information
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Event
from event import serializers


class EventViewSet(viewsets.ModelViewSet):
    """View for managing event information"""
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve event objects for authenticated users."""
        return self.queryset.order_by('-id')
