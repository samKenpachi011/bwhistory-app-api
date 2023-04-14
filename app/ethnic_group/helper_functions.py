"""
Helper functions
"""
from django.contrib.auth import get_user_model

from core import models


def create_user(**params):
    """Create and return a user"""

    return get_user_model().objects.create_user(**params)


# ethinic group
def create_ethnic_group(user, **params):
    """Create and return a ethnic group object"""
    defaults = {
        'name': 'Tswana',
        'description': 'The Tswana are a Bantu-speaking ethnic group',
        'language': 'Setswana',
        'population': 10*100,
        'geography': 'Botswana',
        'history': 'A brief history of the Tswana ethnic group.'
    }
    defaults.update(params)

    ethnic_group = models.EthnicGroup.objects.create(user=user, **defaults)
    return ethnic_group
