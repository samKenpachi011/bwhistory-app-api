from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .managers import UserManager
from core.helpers import image_path, document_path
from .choices import (
    EVENT_TYPE_CHOICES,
    CHIEF_TYPE,
    DOCUMENT_TYPE,
    SITE_TYPE)


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
    image = models.ImageField(null=True, upload_to=image_path)

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


# Event model
class Event(models.Model):
    """Class representing events"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    event_type = models.CharField(
        max_length=100,
        blank=True,
        choices=EVENT_TYPE_CHOICES)

    def __str__(self) -> str:
        return self.name


class EventImages(models.Model):
    """Class representing event images"""
    event = models.ForeignKey(
        Event,
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    images = models.ImageField(null=True, upload_to=image_path)


class Chief(models.Model):
    """Class representing chiefs"""
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    ethnic_group = models.ForeignKey(
        EthnicGroup, related_name="ethnicgroup",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    type = models.CharField(
        max_length=100,
        blank=True,
        choices=CHIEF_TYPE)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_appointment = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


# Publisher Model
class Publisher(models.Model):
    """Class representing published documents"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    document_type = models.CharField(
        max_length=100,
        blank=True,
        choices=DOCUMENT_TYPE)
    document = models.FileField(upload_to=document_path,
                                null=True, blank=True)
    is_published = models.BooleanField(default=False)


# Site model
class Site(models.Model):
    site_name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    ethnic_group = models.ForeignKey(
        EthnicGroup,
        on_delete=models.SET_NULL, null=True, blank=True)
    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL, null=True, blank=True)
    site_type = models.CharField(max_length=20, choices=SITE_TYPE)
    importance = models.PositiveIntegerField(default=1, blank=True, null=True)
    sensitivity = models.PositiveIntegerField(default=1, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        default=1, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        default=1, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.site_name


class SiteImages(models.Model):
    """Class representing site images"""
    site = models.ForeignKey(
        Site,
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    images = models.ImageField(null=True, upload_to=image_path)
