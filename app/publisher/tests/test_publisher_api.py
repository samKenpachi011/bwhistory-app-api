"""
Test publisher api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import Publisher


PUBLISHER_URL = reverse('publisher:publisher-list')


def create_document(user, **params):
    """Create and return a publisher object"""

    defaults = {
        'document': 'example2.pdf',
        'document_type': 'article'
    }

    document = Publisher.objects.create(user=user, **defaults)
    return document


class PublicPublisherTests(TestCase):
    """Tests for unauthenticated users"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(PUBLISHER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePublisherTests(TestCase):
    """Tests authenticated users"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_documents(self):
        """Test retrieve publisher documents"""

        # create publisher object
        create_document(user=self.user)
        res = self.client.get(PUBLISHER_URL)
        # retrieve all objects
        documents = Publisher.objects.all().order_by('-id')
        # pass data to the serializer

        # assert status code == 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(documents.count(), 1)
