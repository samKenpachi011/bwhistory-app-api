"""
Test ethnic group api's
"""
from django.test import TestCase
from django.urls import reverse
import tempfile
import os

from PIL import Image

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from core.models import EthnicGroup, Tag

from ethnic_group.serializers import (
    EthnicGroupSerializer,
    EthnicGroupDetailSerializer)


ETHNIC_GROUP_URL = reverse('ethnic_group:ethnic_group-list')


def image_upload_url(group_id):
    """Create and return an image upload URL."""
    return reverse('ethnic_group:ethnic_group-upload-image', args=[group_id])


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

    def test_create_ethnic_group_with_new_tags(self):
        """Test creating ethnic group with new tags"""

        payload = {
            'name': 'Bakalanga',
            'description': 'The Kalanga are a Bantu-speaking ethnic group.',
            'language': 'Kalanga',
            'population': 100,
            'geography': 'South Africa, Botswana, Zimbabwe',
            'history': 'A brief history of the Bakalanga ethnic group.',
            'tags': [{'name': 'tag1'}, {'name': 'tag2'}],
        }

        res = self.client.post(ETHNIC_GROUP_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ethnic_group = EthnicGroup.objects.all()

        self.assertEqual(ethnic_group.count(), 1)
        self.assertEqual(ethnic_group[0].tags.count(), 2)

        for tag in payload['tags']:
            exist = ethnic_group[0].tags.filter(
                name=tag['name']).exists()
            self.assertTrue(exist)

    def test_create_ethinic_group_with_existing_tags(self):
        """Test creating a new ethinic group with existing tags"""
        tag1 = Tag.objects.create(name='tag1 test', user=self.user)

        payload = {
            'name': 'Bakalanga',
            'description': 'The Kalanga are a Bantu-speaking ethnic group.',
            'language': 'Kalanga',
            'population': 100,
            'geography': 'South Africa, Botswana, Zimbabwe',
            'history': 'A brief history of the Bakalanga ethnic group.',
            'tags': [{'name': 'tag1 test'}, {'name': 'tag2'}],
        }

        res = self.client.post(ETHNIC_GROUP_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ethnic_group = EthnicGroup.objects.all()

        self.assertEqual(ethnic_group.count(), 1)
        self.assertEqual(ethnic_group[0].tags.count(), 2)
        self.assertIn(tag1, ethnic_group[0].tags.all())

        for tag in payload['tags']:
            exist = ethnic_group[0].tags.filter(
                name=tag['name']).exists()
            self.assertTrue(exist)

    def test_create_tag_on_group_update(self):
        """Test creating a new tag on group update"""

        ethnic_group_1 = create_ethnic_group(user=self.user)
        url = detail_url(ethnic_group_1.id)

        payload = {'tags': [{'name': 'tag3'}]}

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ethnic_group = EthnicGroup.objects.all()
        new_tag = Tag.objects.get(user=self.user, name='tag3')
        self.assertIn(new_tag, ethnic_group[0].tags.all())

    def test_clear_tag(self):
        """Test clearing a tag"""

        tag = Tag.objects.create(user=self.user, name='tag test')
        ethnic_group = create_ethnic_group(user=self.user)

        ethnic_group.tags.add(tag)

        payload = {'tags': []}

        url = detail_url(ethnic_group.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(tag, ethnic_group.tags.all())

    def test_filter_by_tag(self):
        """Test filtering groups by tag"""
        group1 = create_ethnic_group(user=self.user, name='Group 1')
        group2 = create_ethnic_group(user=self.user, name='Group 2')

        tag1 = Tag.objects.create(user=self.user, name='tag1')
        tag2 = Tag.objects.create(user=self.user, name='tag2')
        group1.tags.add(tag1)
        group2.tags.add(tag2)
        group3 = create_ethnic_group(user=self.user, name='Group 3')

        params = {'tags': f'{tag1.id}, {tag2.id}'}

        res = self.client.get(ETHNIC_GROUP_URL, params)

        s1 = EthnicGroupSerializer(group1)
        s2 = EthnicGroupSerializer(group2)
        s3 = EthnicGroupSerializer(group3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)


class ImageUploadTests(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.client = APIClient()

        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123')

        self.client.force_authenticate(self.user)

        self.ethnic_group = create_ethnic_group(user=self.user)

    def test_image_upload(self):
        """Test image upload"""

        url = image_upload_url(self.ethnic_group.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}

            res = self.client.post(url, payload, format='multipart')

        self.ethnic_group.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.ethnic_group.image.path))

    def test_upload_image_fail(self):
        """Test image upload failure"""
        url = image_upload_url(self.ethnic_group.id)
        payload = {'image': 'noImage'}

        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
