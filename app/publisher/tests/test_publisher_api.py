"""
Test publisher api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import Publisher
from django.core.files.uploadedfile import SimpleUploadedFile
import os

PUBLISHER_URL = reverse('publisher:publisher-list')


def create_document(user, **params):
    """Create and return a publisher object"""

    defaults = {
        'document': 'example2.pdf',
        'document_type': 'article'
    }

    document = Publisher.objects.create(user=user, **defaults)
    return document


def details_url(document_id):
    """Returns the document details url"""
    return reverse('publisher:publisher-detail', args=[document_id])


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
        create_document(user=self.user)
        res = self.client.get(PUBLISHER_URL)

        documents = Publisher.objects.all().order_by('-id')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(documents.count(), 1)

    def test_create_document(self):
        """Test create publisher document"""
        payload = {
            'document': SimpleUploadedFile(
                'file.pdf',
                b'file_content',
                content_type='application/pdf'
            ),
            'document_type': 'chapter'
        }

        res = self.client.post(PUBLISHER_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        document = Publisher.objects.filter(id=res.data['id'])
        self.assertIn('document', res.data)
        self.assertTrue(os.path.exists(document[0].document.path))

    def test_create_document_fail(self):
        """Test creating fail"""
        payload = {
            'document': SimpleUploadedFile(
                'file2.txt',
                b'file_content',
                content_type='application/pdf'
            ),
            'document_type': 'chapter'
        }

        res = self.client.post(PUBLISHER_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('document', res.data)

    def test_full_publisher_update(self):
        """Test full publisher update"""
        document = create_document(user=self.user)
        url = details_url(document.id)

        payload = {
            'document': SimpleUploadedFile(
                'example3.pdf',
                b'file_content',
                content_type='application/pdf'
            ),
            'document_type': 'chapter'
        }
        res = self.client.patch(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        document.refresh_from_db()
        self.assertEqual(document.document_type, payload['document_type'])

    def test_partial_publisher_update(self):
        """Test partial publisher update"""
        document = create_document(user=self.user)
        url = details_url(document.id)

        payload = {
            'document_type': 'chapter'
        }
        res = self.client.patch(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        document.refresh_from_db()
        self.assertEqual(document.document_type, payload['document_type'])

    def test_document_delete(self):
        """Test deleting publisher object"""
        document = create_document(user=self.user)
        url = details_url(document.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
