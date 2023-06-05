from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import EthnicGroup, Chief
from chief.serializers import ChiefSerializer

CHIEF_URL = reverse('chief:chief-list')


def create_chief(user, **params):
    """Create and return a new chief"""

    group_defaults = {
        'name': 'Tswana',
        'description': 'The Tswana are a Bantu-speaking ethnic group',
        'language': 'Setswana',
        'population': 100,
        'geography': 'Botswana',
        'history': 'A brief history of the Tswana ethnic group.'
    }

    ethnic_group = EthnicGroup.objects.create(
        user=user,
        **group_defaults
    )
    defaults = {
        'name': 'Chief 1',
        'ethnic_group': ethnic_group,
        'type': 'paramount',
        'date_of_birth': '1980-01-01',
        'date_of_appointment': '2000-01-01',
        'is_current': True,
        'bio': 'Event description',
    }

    chief = Chief.objects.create(user=user, **defaults)
    return chief


class PublicChiefAPITests(TestCase):
    """Tests for unauthorized users"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(CHIEF_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateChiefAPITests(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.client = APIClient()

        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_chief(self):
        """Test retrieve chief objects"""

        create_chief(user=self.user)

        res = self.client.get(CHIEF_URL)

        chief = Chief.objects.all().order_by('-id')

        serializer = ChiefSerializer(chief, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
