"""
Tests for the tags API.
"""
from core.helpers import create_user

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.helpers import coremodels
from ethnic_group.serializers import TagsSerializer

TAGS_URL = reverse('ethnic_group:tag-list')


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
        self.user = create_user(email="testuser@example.com", password="testpassword123")

        self.client.force_authenticate(self.user)


    def test_retrieve_tags(self):
        """Retrieve tags"""

        coremodels.Tag.objects.create(name="test tag 1", user=self.user)
        coremodels.Tag.objects.create(name="test tag 2", user=self.user)

        res = self.client.get(TAGS_URL)

        tags = coremodels.Tag.objects.all().order_by("-name")
        serializer = TagsSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

