"""
Test event api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import Event
from event.serializers import EventSerializer


EVENT_URL = reverse('event:event-list')


def create_event(user, **params):
    """Create and return a new event"""

    defaults = {
        'name': 'Event 1',
        'description': 'Event description',
        'event_type': 'Festive',
    }

    event = Event.objects.create(user=user, **defaults)
    return event


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

        self.event = create_event(user=self.user)

    def test_retrieve_event(self):
        """Test retrieve event"""
        create_event(user=self.user)

        res = self.client.get(EVENT_URL)

        events = Event.objects.all().order_by('-id')

        serializer = EventSerializer(events, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
