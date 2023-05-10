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
    serializer_class = serializers.CultureSerializer
    queryset = Culture.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-id')