"""
Test culture api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Culture, EthnicGroup
from culture.serializers import CultureSerializer


CULTURE_URL = reverse('culture:culture-list')


def create_culture(user, **params):
    """Create a new culture"""
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
        'name': 'Test Culture',
        'description': 'Test description',
        'ethnic_group': ethnic_group
    }

    culture = Culture.objects.create(user=user, **defaults)
    return culture


class PublicCultureTests(TestCase):
    """Tests for unauthenticated users."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Tests for authentication required."""
        res = self.client.get(CULTURE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCultureTests(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword')

        defaults = {
            'name': 'Test Tswana',
            'description': 'The Tswana are a Bantu-speaking ethnic group',
            'language': 'Setswana',
            'population': 100,
            'geography': 'Botswana',
            'history': 'A brief history of the Tswana ethnic group.'
        }

        self.ethnic_group = EthnicGroup.objects.create(
            user=self.user,
            **defaults
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_culture(self):
        """Test for retrieving culture information"""

        create_culture(self.user)
        create_culture(self.user)

        res = self.client.get(CULTURE_URL)

        cultures = Culture.objects.all().order_by('-id')

        serializer = CultureSerializer(cultures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_culture(self):
        """Test for creating culture information"""
        payload = {
            'name': 'Test Culture',
            'description': 'Test description',
        }
        res = self.client.post(CULTURE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # compare attributes with payload data
        culture = Culture.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(culture, k), v)

        self.assertEqual(self.user, culture.user)
