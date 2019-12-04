import string
from random import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from user import CustomUser


# Create your models here.

class Settings(models.Model):
    blog_title = models.CharField('blog title', max_length=20, null=False)
    blog_subtitle = models.CharField('blog subtitle', max_length=100, null=True)
    blog_description = models.TextField('blog description', null=True)
    comments_allowed = models.BooleanField('comments allowed', null=False)
    comments_manual_valuation = models.BooleanField(null=False)


class Category(models.Model):
    name = models.CharField('name', max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.name


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


def get_attachment_path():
    return 'attachments/'+random_string(42)+'/'


class Attachment(models.Model):
    file = models.FileField(upload_to=get_attachment_path)
    original_filename = models.CharField(max_length=256, blank=False)


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    default_language = models.BooleanField(null=False)

    def __str__(self):
        return self.name

