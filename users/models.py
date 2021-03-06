from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=1, null=False)
    is_active = models.BooleanField(default=1, null=False)
    date_joined = models.DateTimeField(null=True, blank=True)
    profile_picture = models.FileField(upload_to=CustomUserManager.get_profile_picture_path, null=True, blank=True)
    description = models.ForeignKey('webapp.TranslatableTextgroup', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    description_short = models.ForeignKey('webapp.TranslatableTextgroup', related_name='+', on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELDS = ['email', 'username']
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def natural_key(self):
        return serializers.serialize('json', [self])
