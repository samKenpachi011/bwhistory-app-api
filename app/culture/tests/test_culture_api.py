"""
Test culture api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Culture, EthnicGroup
from culture.serializers import CultureSerializer, CultureDetailsSerializer


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


def details_url(culture_id):
    """Returns the details url"""
    return reverse('culture:culture-detail', args=[culture_id])

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
        res = self.client.post(CULTURE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        culture = Culture.objects.get(id=res.data['id'])
        self.assertEqual(self.user, culture.user)
        self.assertEqual(payload['name'], culture.name)

    def test_create_culture_with_ethnic_group(self):
        """Test for creating culture with ethnic group."""
        payload = {
            'name': 'Test Culture',
            'description': 'Test description',
            'ethnic_group': self.ethnic_group.id
        }
        res = self.client.post(CULTURE_URL, payload, format='json')

        serializer = CultureSerializer(data=payload)
        self.assertTrue(serializer.is_valid())

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        culture = Culture.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if k == 'ethnic_group':
                self.assertEqual(getattr(culture, k).id, v)
            else:
                self.assertEqual(getattr(culture, k), v)

        self.assertEqual(self.user, culture.user)

    def test_get_culture_details(self):
        """Test get culture details"""

        culture = create_culture(user=self.user)
        url = details_url(culture.id)

        res = self.client.get(url)

        serializer = CultureDetailsSerializer(culture)

        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test partial culture update"""

        culture = create_culture(user=self.user)

        payload = {
            'description': 'New description'
        }

        url = details_url(culture.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        culture.refresh_from_db()
        self.assertEqual(culture.description, payload['description'])

    def test_full_culture_update(self):
        """Test full culture update"""

        culture = create_culture(user=self.user)
        payload = {
            'name': 'Updated Culture',
            'description': 'Update description',
            'ethnic_group': self.ethnic_group.id
        }

        url = details_url(culture.id)
        res = self.client.patch(url, payload)

        culture.refresh_from_db()

        self.assertEqual(culture.user, self.user)
        for k,v in payload.items():

            if k == 'ethnic_group':
                self.assertEqual(getattr(culture, k).id, v)
            else:
                self.assertEqual(getattr(culture, k), v)

    def test_detele_culture(self):
        """Test delete culture"""

        culture = create_culture(user=self.user)
        url = details_url(culture.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Culture.objects.filter(id=culture.id).exists())
