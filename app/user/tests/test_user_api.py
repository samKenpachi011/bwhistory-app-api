"""
User API tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_API = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


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

    def test_create_token_success(self):
        """Test create token"""
        user_details = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'name': 'Test Name'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials_error(self):
        """Test create token with bad credentials"""

        user_details = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'name': 'Test Name'
        }

        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test Name'
        }

        create_user(**user_details)

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found_error(self):
        """Test create token email not found"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password_error(self):
        """Test create token without password"""

        payload = {
            'email': 'testuser@example.com',
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_access_unathorized_error(self):
        """Test user profile unathorized access"""

        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test authorized api requests by users"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpassword123',
            name='Test Name'
        )

        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """Test retrieving user profile"""

        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_update_profile_success(self):
        """Test profile update"""
        payload = {
            'name': 'Test Update',
            'password': 'password123',
        }

        res = self.client.patch(PROFILE_URL, payload)

        # refresh the db
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_to_profile_error(self):
        """Test posting to the user profile"""
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
