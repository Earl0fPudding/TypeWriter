import string
from random import random

from django.db import models
from django.contrib.auth.models import AbstractUser

from users.models import CustomUser


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
    return 'attachments/' + random_string(42) + '/'


class Attachment(models.Model):
    file = models.FileField(upload_to=get_attachment_path)
    original_filename = models.CharField(max_length=256, blank=False)


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    name_short = models.CharField(max_length=10, unique=True, blank=False)
    default_language = models.BooleanField(null=False)

    def __str__(self):
        return self.name


class Entry(models.Model):
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE, related_name='entries')
    author = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='entries')


class Content(models.Model):
    title = models.CharField(max_length=256, blank=False)
    summary = models.CharField(max_length=200, blank=False)
    text = models.TextField(blank=False)
    creation_date = models.DateTimeField(null=False)
    last_edit_date = models.DateTimeField(null=True)
    attachments = models.ManyToManyField(Attachment, related_name='contents')
    language = models.ForeignKey(Language, null=False, on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author_name = models.CharField(max_length=80, null=True)
    author_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=False)
    passed = models.BooleanField(null=False)
    publish_date = models.DateTimeField(null=False)
    content = models.ForeignKey(Content, null=False, on_delete=models.CASCADE, related_name='comments')
    answer_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text
