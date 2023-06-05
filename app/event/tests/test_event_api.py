"""
Test event api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import Event, EventImages
import tempfile
import os
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


def get_image():
    """Creates and return an image"""
    image = Image.new("RGB", (10, 10))
    file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(file, format='JPEG')
    _file = open(file.name, 'rb')
    return _file


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
            'name': 'Event 9',
            'description': 'Event description',
            'event_type': 'festive',
        }

        res = self.client.post(EVENT_URL, payload, format='multipart')

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

        res = self.client.patch(url, payload, format='multipart')

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

    def test_image_upload_with_existing_event(self):
        """Test event image upload with existing event"""
        url = details_url(self.event.id)
        payload = {
            'uploaded_images': [get_image(), get_image()]
        }

        res = self.client.patch(url, payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_image_upload_with_new_event(self):
        """Test event image upload on event create"""
        payload = {
            'name': 'Event 3',
            'description': 'Event description',
            'event_type': 'festive',
            'uploaded_images': [get_image(), get_image()]
        }

        res = self.client.post(EVENT_URL, payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        event_imgs = EventImages.objects.filter(event_id=res.data['id'])
        self.assertIn('images', res.data)
        self.assertTrue(os.path.exists(event_imgs[0].images.path))
