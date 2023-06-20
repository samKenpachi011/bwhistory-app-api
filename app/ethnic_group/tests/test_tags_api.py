"""
Tests for the tags API.
"""
from core.helpers import create_user

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, EthnicGroup
from ethnic_group.serializers import TagsSerializer

TAGS_URL = reverse('ethnic_group:tag-list')


def detail_url(tag_id):
    """Create and return a detail URL for a given tag"""

    return reverse('ethnic_group:tag-detail', args=[tag_id])


class PublicTagsApiTests(TestCase):
    """Public tags API tests"""
    def setUp(self):
        self.client = APIClient()

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Private tags API tests"""

    def setUp(self):

        self.client = APIClient()
        self.user = create_user(
            email="testuser@example.com",
            password="testpassword123")

        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Retrieve tags"""

        Tag.objects.create(name="test tag 1", user=self.user)
        Tag.objects.create(name="test tag 2", user=self.user)

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagsSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_tags(self):
        """Test updating tags"""

        tag = Tag.objects.create(name="test tag 1", user=self.user)
        url = detail_url(tag.id)

        payload = {'name': 'tag update'}

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting tag"""

        tag = Tag.objects.create(name='test tag 1', user=self.user)

        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_assigned_to_groups(self):
        """Test filtering tags assigned to groups"""

        tag1 = Tag.objects.create(user=self.user, name='tag1')
        tag2 = Tag.objects.create(user=self.user, name='tag2')

        ethnic_group = EthnicGroup.objects.create(
            user=self.user,
            name='Bakalanga',
            description='The Kalanga are a Bantu-speaking ethnic group.',
            language='Kalanga',
            population=100,
            geography='South Africa, Botswana, Zimbabwe',
            history='A brief history of the Bakalanga ethnic group.',
        )

        ethnic_group.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        s1 = TagsSerializer(tag1)
        s2 = TagsSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique_(self):
        """Test that filtered tags are not duplicate"""
        tag1 = Tag.objects.create(user=self.user, name='tag1')
        Tag.objects.create(user=self.user, name='tag2')

        ethnic_group1 = EthnicGroup.objects.create(
            user=self.user,
            name='Group 1',
            description='Test',
            language='Test',
            population=100,
            geography='South Africa, Botswana, Zimbabwe',
            history='A brief history of the test ethnic group.',
        )
        ethnic_group2 = EthnicGroup.objects.create(
            user=self.user,
            name='Group 2',
            description='Test',
            language='Test',
            population=100,
            geography='South Africa, Botswana, Zimbabwe',
            history='A brief history of the test ethnic group.',
        )

        ethnic_group1.tags.add(tag1)
        ethnic_group2.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
