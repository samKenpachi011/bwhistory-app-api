"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_successful(self):
        """Test creating a user with all values"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)

# check whether the plaintext password is equivalent to the hashed password.
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'pass123')
            self.assertEqual(user.email, expected)

    def test_user_without_email_raise_error(self):
        """Test email not empty"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_creating_superuser(self):
        """Test to create a super user"""

        user = get_user_model().objects.create_superuser(
            'admin@example.com', 'testpassword123')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_creating_ethnic_group_success(self):
        """Test to create a ethnic group object"""

        # define the user
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        name = 'Tswana'
        description = 'The Tswana are a Bantu-speaking ethnic group'
        language = 'Setswana'
        population = 10*100
        geography = 'Botswana'
        history = 'A brief history of the Tswana ethnic group.'

        ethnic_group = models.EthnicGroup.objects.create(
            user=user,
            name=name,
            description=description,
            language=language,
            population=population,
            geography=geography,
            history=history
        )
        self.assertEqual(str(ethnic_group), ethnic_group.name)
