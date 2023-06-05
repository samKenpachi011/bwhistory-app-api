from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import EthnicGroup, Chief
from chief.serializers import ChiefSerializer, ChiefDetailsSerializer

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


def details_url(chief_id):
    """Returns the chief details url"""
    return reverse('chief:chief-detail', args=[chief_id])


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

    def test_create_chief(self):
        """Test create chief"""

        payload = {
            'name': 'Chief test 2',
            'type': 'paramount',
            'date_of_birth': '1980-01-01',
            'date_of_appointment': '2000-01-01',
            'is_current': True,
            'bio': 'Event description',
        }

        res = self.client.post(CHIEF_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        chief = Chief.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], chief.name)

    def test_create_chief_with_ethnic_group(self):
        """Test creating a chief object with ethnic group"""
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

        payload = {
            'name': 'Chief test 2',
            'ethnic_group': self.ethnic_group.id,
        }

        res = self.client.post(CHIEF_URL, payload, format='json')
        serialzier = ChiefSerializer(data=payload)
        self.assertTrue(serialzier.is_valid())

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        chief = Chief.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if k == 'ethnic_group':
                self.assertEqual(getattr(chief, k).id, v)
            else:
                self.assertEqual(getattr(chief, k), v)

        self.assertEqual(self.user, chief.user)

    def test_partial_update(self):
        """Test partial chief update"""
        chief = create_chief(user=self.user)
        url = details_url(chief.id)
        payload = {'name': 'Test Update'}

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        chief.refresh_from_db()
        self.assertEqual(payload['name'], chief.name)

    def test_full_chief_update(self):
        """Test full chief update"""
        chief = create_chief(user=self.user)
        url = details_url(chief.id)

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

        payload = {
            'name': 'Test full update',
            'ethnic_group': self.ethnic_group.id,
        }

        self.client.patch(url, payload)
        chief.refresh_from_db()

        for k, v in payload.items():
            if k == 'ethnic_group':
                self.assertEqual(getattr(chief, k).id, v)
            else:
                self.assertEqual(getattr(chief, k), v)

    def test_get_chief_details(self):
        """Test get chief details"""
        chief = create_chief(user=self.user)
        url = details_url(chief.id)

        res = self.client.get(url)

        serializer = ChiefDetailsSerializer(chief)
        self.assertEqual(res.data, serializer.data)

    def test_delete_chief(self):
        """Test delete chief object"""
        chief = create_chief(user=self.user)

        url = details_url(chief.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Chief.objects.filter(id=chief.id).exists())
