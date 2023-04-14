"""
Test ethnic group api's
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from ethnic_group import helper_functions as hf


ETHNIC_GROUP_URL = reverse(
    'ethnic_group:ethnic-group-list')


class PublicEthnicGroupTests(TestCase):
    """Tests for unathenticated users"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""

        res = self.client.get(ETHNIC_GROUP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEthnicGroupTests(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.client = APIClient()

        self.user = hf.create_user(
            email='testuser@example.com',
            password='testpassword123')

        self.client.force_authenticate(self.user)

    def test_create_ethnic_group(self):
        """
        Test creating a new EthnicGroup object.
        """
        payload = {
            'name': 'Bakalanga',
            'description': 'The Kalanga are a Bantu-speaking ethnic group.',
            'language': 'Kalanga',
            'population': 11 * 10**6,
            'geography': 'South Africa, Botswana, Zimbabwe',
            'history': 'A brief history of the Bakalanga ethnic group.',
        }
        res = self.client.post(ETHNIC_GROUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(hf.models.EthnicGroup.objects.count(), 1)

        ethnic_group = hf.models.EthnicGroup.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(ethnic_group, k), v)

        self.assertEqual(self.user, ethnic_group.user)

    def test_retrieve_group(self):
        """Test listing ethnic groups"""
