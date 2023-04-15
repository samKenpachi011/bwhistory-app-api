"""
Test ethnic group api's
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from core.models import EthnicGroup

from ethnic_group.serializers import (
    EthnicGroupSerializer,
    EthnicGroupDetailSerializer)


ETHNIC_GROUP_URL = reverse('ethnic_group:ethnic_group-list')


def create_user(**params):
    """Create and return a user"""

    return get_user_model().objects.create_user(**params)


# ethinic group
def create_ethnic_group(user, **params):
    """Create and return a ethnic group object"""
    defaults = {
        'name': 'Tswana',
        'description': 'The Tswana are a Bantu-speaking ethnic group',
        'language': 'Setswana',
        'population': 100,
        'geography': 'Botswana',
        'history': 'A brief history of the Tswana ethnic group.'
    }
    defaults.update(params)

    ethnic_group = EthnicGroup.objects.create(user=user, **defaults)
    return ethnic_group


def detail_url(group_id):
    """Create and return a ethnic group detail URL."""
    return reverse('ethnic_group:ethnic_group-detail', args=[group_id])


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

        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123')

        self.client.force_authenticate(self.user)

    def test_retrieve_group(self):
        """Test listing ethnic groups"""

        create_ethnic_group(user=self.user)
        create_ethnic_group(user=self.user)

        res = self.client.get(ETHNIC_GROUP_URL)

        ethnic_groups = EthnicGroup.objects.all().order_by('-id')

        # passing a list of objects to the serializer
        serializer = EthnicGroupSerializer(ethnic_groups, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ethnic_group(self):
        """
        Test creating a new EthnicGroup object.
        """
        payload = {
            'name': 'Bakalanga',
            'description': 'The Kalanga are a Bantu-speaking ethnic group.',
            'language': 'Kalanga',
            'population': 100,
            'geography': 'South Africa, Botswana, Zimbabwe',
            'history': 'A brief history of the Bakalanga ethnic group.',
        }
        res = self.client.post(ETHNIC_GROUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ethnic_group = EthnicGroup.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(ethnic_group, k), v)

        self.assertEqual(self.user, ethnic_group.user)

    def test_get_ethnic_group_details(self):
        """Get details of a group"""

        ethnic_group = create_ethnic_group(user=self.user)
        url = detail_url(ethnic_group.id)

        res = self.client.get(url)

        # pass the object through the serializer
        serializer = EthnicGroupDetailSerializer(ethnic_group)

        self.assertEqual(res.data, serializer.data)
