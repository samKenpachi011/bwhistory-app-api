"""
Tests for models
"""
from django.test import TestCase, tag
from unittest.mock import patch
from core import models
from core.helpers import (
    get_user_model,
    create_user,
    image_path,
    document_path)
import datetime


@tag('mdls')
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

    def test_create_tag_success(self):
        """Test creating a tag success"""
        user = create_user(
            email='test@example.com',
            password='testpassword123')
        tag = models.Tag.objects.create(user=user, name='testtag')

        self.assertEqual(str(tag), tag.name)

# Culture model tests
    def test_creating_culture_success(self):
        """Test creating culture success"""

        # define the user
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        # define the culture
        ethnic_group = models.EthnicGroup.objects.create(
            user=user,
            name='Tswana',
            description='The Tswana are a Bantu-speaking ethnic group',
            language='Setswana',
            population=10*100,
            geography='Botswana',
            history='A brief history of the Tswana ethnic group.'
        )

        culture = models.Culture.objects.create(
            user=user,
            ethnic_group=ethnic_group,
            name='Test Culture',
            description='Test culture'
        )

        self.assertEqual(str(culture), culture.name)

# Events model
    def test_creating_event_sucsess(self):
        """Test creating event"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        event = models.Event.objects.create(
            user=user,
            name='Test Event',
            description='Test Event',
            event_type='traditional',
        )

        self.assertEqual(str(event), event.name)

    @patch('uuid.uuid4')
    def test_event_image_success(self, mock_uuid):
        """Test event image upload"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        self.event = models.Event.objects.create(
            user=user,
            name='Test Event',
            description='Test Event',
            event_type='traditional',
        )

        event_images = models.EventImages.objects.create(
            event=self.event,
            images='example.jpg',
        )
        path = '/vol/web/media/example.jpg'
        self.assertEqual(event_images.event, self.event)
        self.assertEqual(event_images.images.path, f'{path}')

# Chiefs model

    def test_create_chief_success(self):
        """Test creating a chief object success"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        self.ethnic_group = models.EthnicGroup.objects.create(
            user=user,
            name='Tswana',
            description='The Tswana are a Bantu-speaking ethnic group',
            language='Setswana',
            population=0*100,
            geography='Botswana',
            history='A brief history of the Tswana ethnic group.'
        )

        chief_test = models.Chief.objects.create(
            name='Chief Test',
            ethnic_group=self.ethnic_group,
            type='paramount',
            date_of_birth='1980-01-01',
            date_of_appointment='2000-01-01',
            is_current=True,
            bio='Test bio',
        )

        self.assertEqual(str(chief_test), chief_test.name)

# Generic image path test
    @patch('uuid.uuid4')
    def test_image_path(self, mock_uuid):
        """Test creating an image path for instances"""

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = image_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/test/{uuid}.jpg')

# Publisher model
    @patch('uuid.uuid4')
    def test_publisher_publish_success(self, mock_uuid):
        """Test publisher upload"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        published_document = models.Publisher.objects.create(
            user=user,
            document='example.pdf',
            document_type='article',
        )
        path = '/vol/web/media/example.pdf'

        self.assertEqual(published_document.document.path, f'{path}')

# Generic document path test
    @patch('uuid.uuid4')
    def test_document_path(self, mock_uuid):
        """Test creating an document path for instances"""

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        doc_path = document_path(None, 'example.pdf')
        dt = datetime.datetime.now()
        milliseconds = dt.strftime('%f')[:-4]
        dt = dt.strftime('%Y-%m-%dT%H:%M:%S')
        df = f'{dt}{milliseconds}'

        self.assertEqual(doc_path, f'uploads/documents/{uuid}{df}.pdf')
