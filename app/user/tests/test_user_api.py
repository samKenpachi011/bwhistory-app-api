"""
User API tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_API = reverse('user:create')


# helper function
def create_user(**params):
    """Create and return user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Public user api tests"""

    def setUp(self):

        self.client = APIClient()

    def test_user_create_success(self):
        """Test create user api"""
        # payload to pass in the request
        payload = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_API, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get user and check credentials
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('assword', res.data)

    def test_user_exists_error(self):
        """Test user exists"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'name': 'Test Name'
        }

        # call the create user
        create_user(**payload)

        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """est error returned if password is too short"""

        payload = {
            'email': 'test@example.com',
            'password': '123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # check if the user is created
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)
