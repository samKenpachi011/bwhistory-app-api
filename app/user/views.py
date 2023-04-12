"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a user"""

    serializer_class = UserSerializer


class CreateAuthTokenView(ObtainAuthToken):

    serializer_class = AuthTokenSerializer
    # allow you to return responses with various media type
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
