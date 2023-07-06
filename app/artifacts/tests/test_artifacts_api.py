from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.helpers import create_user
from core.models import (
    EthnicGroup,
    Culture,
    Site,
    Artifacts)
from artifacts.serializers import ArtifactsSerializer


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
