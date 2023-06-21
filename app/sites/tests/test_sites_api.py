"""
Test sites api's
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import (
    EthnicGroup,
    Culture,
    Site)


SITES_URL = reverse('sites:sites-list')


def create_site(user, **params):
    """Create and return a Site"""
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

    culture_defaults = {
        'name': 'Test Culture',
        'description': 'Test description',
        'ethnic_group': ethnic_group
    }

    culture = Culture.objects.create(user=user, **culture_defaults)

    defaults = {
        'site_name': 'Test Site 2',
        'ethnic_group': ethnic_group,
        'culture': culture,
        'site_type': 'cultural',
        'importance': 1,
        'sensitivity': 1,
        'latitude': -24.653257,
        'longitude': 25.906792,
        'description': 'Test Site 2 description',
    }

    defaults.update(params)

    site = Site.objects.create(
        user=user,
        **defaults
    )

    return site


class PublicSitesTestCase(TestCase):
    """Tests for unauthenticated users"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(SITES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSitesTestCase(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_sites(self):
        """Test retrieve all sites"""
        create_site(user=self.user)

        res = self.client.get(SITES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        sites = Site.objects.all()
        self.assertEqual(sites.count(), 1)
