import uuid
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .managers import UserManager
from core.helpers import image_path


def ethnic_group_image_path(instance, filename):
    """Generate file path for ethnic group image"""

    # get the extension of the image
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'ethnic_group', filename)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # define the unique identifier for the
    USERNAME_FIELD = 'email'

    # specify that all objects come from the manager
    objects = UserManager()

    def __str__(self):
        return self.email


class EthnicGroup(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=100, blank=True)
    population = models.PositiveIntegerField()
    geography = models.CharField(max_length=200, blank=True)
    history = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=ethnic_group_image_path)

    class Meta:
        verbose_name_plural = "Ethnic Groups"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Class representing tags"""
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


# Culture model
class Culture(models.Model):
    """Class representing cultures"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    ethnic_group = models.ForeignKey(
        EthnicGroup, related_name="ethnic_group",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=image_path)

    def __str__(self):
        return self.name
