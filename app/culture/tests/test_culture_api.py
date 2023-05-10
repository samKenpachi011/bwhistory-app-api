"""
Test culture api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model # noqa


CULTURE_URL = reverse('culture:culture-list')


class PublicCultureTests(TestCase):
    """Tests for unauthenticated users."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Tests for authentication required."""
        res = self.client.get(CULTURE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
