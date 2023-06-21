"""
Test sites api's
"""
from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import (
    EthnicGroup,
    Culture,
    Site)
from sites.serializers import SiteDetailsSerializer


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
        'importance': 2,
        'sensitivity': 2,
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


def details_url(site_id):
    """Returns site details"""
    return reverse('sites:sites-detail', args=[site_id])


class PublicSitesTestCase(TestCase):
    """Tests for unauthenticated users"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(SITES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


@tag('pst')
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

    def test_create_site(self):
        """Test creating a new site"""

        payload = {
            'site_name': 'Test Site 4',
            'site_type': 'cultural',
        }

        res = self.client.post(SITES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        site = Site.objects.get(id=res.data['id'])
        self.assertEqual(payload['site_name'], site.site_name)

    def test_site_details(self):
        """Test get site details"""

        site = create_site(user=self.user)
        url = details_url(site.id)

        res = self.client.get(url)

        serializer = SiteDetailsSerializer(site)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_partial_site_update(self):
        """Test partial site update"""
        site = create_site(user=self.user)
        url = details_url(site.id)
        payload = {
            'site_type': 'natural',
            'description': 'Test Site update'
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        site.refresh_from_db()
        self.assertEqual(payload['site_type'], site.site_type)

    def test_full_site_update(self):
        """Test full site update"""
        site = create_site(user=self.user)
        url = details_url(site.id)

        group2_defaults = {
            'name': 'Group Update',
            'description': 'The Tswana are a Bantu-speaking ethnic group',
            'language': 'Setswana',
            'population': 100,
            'geography': 'Botswana',
            'history': 'A brief history of the Tswana ethnic group.'
        }

        ethnic_group2 = EthnicGroup.objects.create(
            user=self.user,
            **group2_defaults
        )

        culture_defaults2 = {
            'name': 'Test Culture Update',
            'description': 'Test description',
            'ethnic_group': ethnic_group2
        }

        culture2 = Culture.objects.create(user=self.user, **culture_defaults2)

        payload = {
            'site_name': 'Test Site Update',
            'ethnic_group': ethnic_group2.id,
            'culture': culture2.id,
            'site_type': 'natural',
            'importance': 3,
            'sensitivity': 3,
            'latitude': -21.173611,
            'longitude': 27.512501,
            'description': 'Test Site Update description',
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        site.refresh_from_db()
        self.assertEqual(payload['site_type'], site.site_type)

    def test_delete_site(self):
        """Test delete site"""
        site = create_site(user=self.user)
        url = details_url(site.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Site.objects.filter(id=site.id).exists())
