"""
Tests for the admin site
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Tests for the admin site"""

    def setUp(self):
        """Set up th user and client"""

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpassword123'
        )

        # force admin user login
        self.client.force_login(self.admin_user)

        # normal user
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            name='testuser'
        )

    def test_admin_list_users(self):
        """Test listing users"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user(self):
        """Test editing user."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_add_user(self):
        """Test  sdding user."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
