"""
Helper functions
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


def create_user(email, password):
    """Create a new user"""
    return get_user_model().objects.create_user(email, password)
