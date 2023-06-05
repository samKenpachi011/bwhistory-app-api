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
    serializer_class = serializers.ChiefSerializer
    queryset = Chief.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns chief objects"""
        return self.queryset.order_by('-id')
