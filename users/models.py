from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(_('email address'), null=True, unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=50, null=True)
    is_staff = None
    is_active = None
    date_joined = models.DateTimeField(null=True)
    profile_picture = models.FileField(upload_to=CustomUserManager.get_profile_picture_path, null=True)
    description = models.TextField(null=True)

    USERNAME_FIELDS = ['email', 'username']
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
