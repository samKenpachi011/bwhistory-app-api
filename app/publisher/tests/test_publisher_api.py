"""
Test publisher api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


PUBLISHER_URL = reverse('publisher:publisher-list')


class PublicPublisherTests(TestCase):
    """Tests for unauthenticated users"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(PUBLISHER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
