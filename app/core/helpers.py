"""
Helper functions
"""

from django.contrib.auth import get_user_model
from core.models import Tag


def create_user(email, password):
    """Create a new user"""
    return get_user_model().objects.create_user(email, password)


def _params_to_ints(self, qs):
    """Convert a list of stings to integers"""
    return [int(x) for x in qs.split(',')]


def _get_or_create(user, tags, instance):
    """Get or create a new tag."""
    for tag in tags:
        tag_object, created = Tag.objects.get_or_create(
            user=user,
            **tag
        )
        instance.tags.add(tag_object)
    return instance
