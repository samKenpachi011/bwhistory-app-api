"""
Test for culture tags
"""
from core.helpers import create_user
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse
from culture.tests.test_culture_api import create_culture
from ethnic_group.serializers import TagsSerializer

from core.models import Tag

TAGS_URL = reverse('culture:tag-list')


class PrivateCultureTags(TestCase):
    """Private tags API tests for culture"""
    def setUp(self):

        self.client = APIClient()
        self.user = create_user(
            email="testuser@example.com",
            password="testpassword123"
        )

        self.client.force_authenticate(self.user)

    def test_filter_tags_assigned_to_culture(self):
        """Test filter tags assigned to culture."""

        tag = Tag.objects.create(user=self.user, name='tag 1')
        tag2 = Tag.objects.create(user=self.user, name='tag 2')

        culture = create_culture(user=self.user)
        culture.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        s1 = TagsSerializer(tag)
        s2 = TagsSerializer(tag2)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
