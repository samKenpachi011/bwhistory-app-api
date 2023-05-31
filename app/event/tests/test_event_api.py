"""
Test event api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import Event
import tempfile
from PIL import Image
from event.serializers import EventSerializer, EventDetailsSerializer


EVENT_URL = reverse('event:event-list')


def create_event(user, **params):
    """Create and return a new event"""

    defaults = {
        'name': 'Event 1',
        'description': 'Event description',
        'event_type': 'festive',
    }

    event = Event.objects.create(user=user, **defaults)
    return event


def details_url(event_id):
    """Returns the details url for a given event"""
    return reverse('event:event-detail', args=[event_id])


def event_upload_image(event_id):
    """Returns the image upload url for a given event"""
    return reverse('event:event-upload-image', args=[event_id])


class PublicEventTests(TestCase):
    """Tests for unauthenticated users."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(EVENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventTests(TestCase):
    """Tests for authenticated users."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_event(self):
        """Test retrieve event"""
        create_event(user=self.user)

        res = self.client.get(EVENT_URL)

        events = Event.objects.all().order_by('-id')

        serializer = EventSerializer(events, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_event(self):
        """Test creating an event"""
        payload = {
            'name': 'Event 2',
            'description': 'Event description',
            'event_type': 'festive',
        }

        res = self.client.post(EVENT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=res.data['id'])
        self.assertEqual(self.user, event.user)
        self.assertEqual(payload['name'], event.name)

    def test_get_event_details(self):
        """Test get event details"""
        event = create_event(user=self.user)
        url = details_url(event.id)

        res = self.client.get(url)

        serializer = EventDetailsSerializer(event)

        self.assertEqual(res.data, serializer.data)

    def test_event_partial_update(self):
        """Test event update"""
        event = create_event(user=self.user)
        url = details_url(event.id)

        payload = {
            'description': 'New description'
        }

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.description, payload['description'])

    def test_event_full_update(self):
        """Test event full update"""

        event = create_event(user=self.user)

        payload = {
            'name': 'Event Test',
            'description': 'New description',
        }
        url = details_url(event.id)

        self.client.patch(url, payload)

        event.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(event, k), v)

    def test_event_delete(self):
        """Test event deletion"""
        event = create_event(user=self.user)
        url = details_url(event.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())


class EventImageUploadTestCase(TestCase):
    """Test for Event Image Uploads"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)
        self.event = create_event(user=self.user)

    def test_event_image_upload_fail(self):
        """Test that an image upload fails"""
        url = event_upload_image(self.event.id)

        payload = {'image': 'no_image'}

        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_image_upload(self):
        """Test an image upload"""
        url = event_upload_image(self.event.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}

            res = self.client.post(url, payload, format='multpart')

            self.event.refresh_from_db()
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn('image', res.data)
