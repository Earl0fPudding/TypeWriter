from django.db import models
from django.contrib.auth.models import AbstractUser


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


def get_profile_picture_path(instance, filename):
    return instance.username+'/profile.png'


class User(AbstractUser):
    description = models.TextField(null=True)
    profile_picture = models.FileField(upload_to=get_profile_picture_path, null=True)

    def __str__(self):
        return self.username

class Attachment(models.Model):
    file = models.FileField(upload_to='')
    original_filename = models.CharField(max_length=256, blank=False)
