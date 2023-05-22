"""
Helper functions
"""

import uuid
import os
from django.contrib.auth import get_user_model
from core import models
from rest_framework.test import APIClient # noqa


def create_user(email, password):
    """Create a new user"""
    return get_user_model().objects.create_user(email, password)


def _params_to_ints(qs):
    """Convert a list of stings to integers"""
    return [int(x) for x in qs.split(',')]


def _get_or_create(user, tags, instance):
    """Get or create a new tag."""
    for tag in tags:
        tag_object, created = models.Tag.objects.get_or_create(
            user=user,
            **tag
        )
        instance.tags.add(tag_object)
    return instance


# generate file path for images
def image_path(instance, filename):
    """Generate a path for instance images"""
    class_name = 'test'

    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    if type(instance) == models.EthnicGroup:
        class_name = 'ethnic_group'
    elif type(instance) == models.Culture:
        class_name = 'culture'
    breakpoint()
    return os.path.join('uploads', class_name, filename)
