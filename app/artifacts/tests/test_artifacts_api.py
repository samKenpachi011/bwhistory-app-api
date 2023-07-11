from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user, get_image
from core.models import (
    EthnicGroup,
    Culture,
    Site,
    Artifacts,
    ArtifactImages)
from artifacts.serializers import (
    ArtifactsSerializer,
    ArtifactsDetailsSerializer)
import os


ARTIFACTS_URL = reverse('artifacts:artifacts-list')


def create_artifact(user, **params):
    """Create a new artifact"""
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

    site_defaults = {
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

    site = Site.objects.create(
        user=user,
        **site_defaults
    )

    defaults = {
        'artifact_name': 'Test Artifact',
        'artifact_type': 'tool',
        'description': 'Test description',
        'historical_significance': 5.0,
        'cultural_significance': 5.0,
        'ethnic_group': ethnic_group,
        'culture': culture,
        'site': site
    }

    defaults.update(params)

    artifact = Artifacts.objects.create(
        user=user, **defaults)

    return artifact


def details_url(artifact_id):
    """Returns the details url"""
    return reverse('artifacts:artifacts-detail', args=[artifact_id])


class PublicArtifactsAPITests(TestCase):
    """Tests for unauthenticated users"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required"""
        res = self.client.get(ARTIFACTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArtifactAPITests(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_artifacts(self):
        """Test retrieving artifact objects"""
        create_artifact(user=self.user)
        create_artifact(user=self.user)

        res = self.client.get(ARTIFACTS_URL)

        artifacts = Artifacts.objects.all().order_by('-id')
        serializer = ArtifactsSerializer(artifacts, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_artifact(self):
        """Tests creating a base artifact"""

        payload = {
           'artifact_name': 'Test Artifact',
           'artifact_type': 'tool',
           'description': 'Test description',
           'historical_significance': 5.0,
           'cultural_significance': 5.0
        }

        res = self.client.post(ARTIFACTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        artifact = Artifacts.objects.get(id=res.data['id'])
        self.assertEqual(self.user, artifact.user)
        self.assertEqual(payload['artifact_name'], artifact.artifact_name)

    def test_get_artifact_details(self):
        """Test get artifact details"""
        artifact = create_artifact(user=self.user)
        url = details_url(artifact.id)
        res = self.client.get(url)

        serializer = ArtifactsDetailsSerializer(artifact)
        self.assertEqual(res.data, serializer.data)

    def test_delete_artifact(self):
        """Test deleting an artifact"""
        artifact = create_artifact(user=self.user)
        url = details_url(artifact.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Artifacts.objects.filter(id=artifact.id).exists())

    def test_partial_artifact_update(self):
        """Test partial update"""
        artifact = create_artifact(user=self.user)
        url = details_url(artifact.id)

        payload = {
            'artifact_name': 'Test Update',
            'artifact_type': 'tool'
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        artifact.refresh_from_db()
        self.assertEqual(payload['artifact_type'], artifact.artifact_type)

    def test_full_artifact_update(self):
        """Test full update"""

        artifact = create_artifact(user=self.user)
        url = details_url(artifact.id)

        group_defaults2 = {
            'name': 'Tswana',
            'description': 'The Tswana are a Bantu-speaking ethnic group',
            'language': 'Setswana',
            'population': 100,
            'geography': 'Botswana',
            'history': 'A brief history of the Tswana ethnic group.'
        }

        ethnic_group2 = EthnicGroup.objects.create(
            user=self.user,
            **group_defaults2
        )

        culture_defaults2 = {
            'name': 'Test Culture',
            'description': 'Test description',
            'ethnic_group': ethnic_group2
        }

        culture2 = Culture.objects.create(user=self.user, **culture_defaults2)

        site_defaults2 = {
            'site_name': 'Test Site 2',
            'ethnic_group': ethnic_group2,
            'culture': culture2,
            'site_type': 'cultural',
            'importance': 2,
            'sensitivity': 2,
            'latitude': -24.653257,
            'longitude': 25.906792,
            'description': 'Test Site 2 description',
        }

        site2 = Site.objects.create(
            user=self.user,
            **site_defaults2
        )

        payload = {
            'artifact_name': 'Test artifact full update',
            'artifact_type': 'tool',
            'description': 'Test full update description',
            'historical_significance': 6.0,
            'cultural_significance': 6.0,
            'ethnic_group': ethnic_group2,
            'culture': culture2,
            'site': site2
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        artifact.refresh_from_db()
        self.assertEqual(payload['artifact_type'], artifact.artifact_type)


class ArtifactImageUploadTests(TestCase):
    """Tests for artifact image upload"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

        self.client.force_authenticate(self.user)
        self.artifact = create_artifact(user=self.user)

    def test_image_upload_with_new_artifact(self):
        """Test image upload with new artifact"""
        payload = {
           'artifact_name': 'Test Artifact',
           'artifact_type': 'tool',
           'description': 'Test description',
           'historical_significance': 5.0,
           'cultural_significance': 5.0,
           'uploaded_images': [get_image(), get_image()]
        }

        res = self.client.post(ARTIFACTS_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        artifact_imgs = ArtifactImages.objects.filter(
            artifact_id=res.data['id'])
        self.assertIn('images', res.data)
        self.assertTrue(os.path.exists(artifact_imgs[0].images.path))

    def test_image_upload_with_existing_artifact(self):
        """Test image upload with existing artifact"""
        url = details_url(self.artifact.id)
        payload = {
            'uploaded_images': [get_image(), get_image()]
        }

        res = self.client.patch(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
