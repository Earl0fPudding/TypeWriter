import os
import string
import random

from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from users.models import CustomUser


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    name_short = models.CharField(max_length=10, unique=True, blank=False)
    default_language = models.BooleanField(null=False)

    def __str__(self):
        return self.name


class TranslatableSmalltext(models.Model):
    def __str__(self):
        if len(TranslatedSmalltext.objects.filter(translatable_smalltext_id=self.id)) > 0:
            return 'TxtSmGrp - "' + TranslatedSmalltext.objects.filter(translatable_smalltext_id=self.id)[0].text + '"'
        else:
            return "Empty SmallTextgroup"


class TranslatedSmalltext(models.Model):
    text = models.CharField(max_length=50, null=False, blank=False)
    translatable_smalltext = models.ForeignKey(TranslatableSmalltext, related_name='translated_smalltexts', null=False,
                                               blank=False, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='translated_smalltexts', null=False, blank=False,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class TranslatableTextgroup(models.Model):
    def __str__(self):
        if len(TranslatedText.objects.filter(translatable_textgroup_id__exact=self.id)) > 0:
            return 'TxtGrp - "' + TranslatedText.objects.filter(translatable_textgroup_id__exact=self.id)[0].text[
                                  :75] + '"'
        else:
            return "Empty Textgroup"


class TranslatedText(models.Model):
    text = RichTextField(null=False, blank=False)
    translatable_textgroup = models.ForeignKey(TranslatableTextgroup, related_name='translated_texts', null=False,
                                               blank=False, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='translated_texts', null=False, blank=False,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:250]


class Settings(models.Model):
    blog_title = models.OneToOneField(TranslatableSmalltext, related_name='+', on_delete=models.CASCADE, blank=False,
                                      null=False)
    blog_subtitle = models.ForeignKey(TranslatableTextgroup, related_name='+', on_delete=models.CASCADE, blank=True,
                                      null=True)
    blog_description = models.ForeignKey(TranslatableTextgroup, related_name='+', on_delete=models.CASCADE, blank=True,
                                         null=True)
    comments_allowed = models.BooleanField('comments allowed', null=False)
    comments_manual_valuation = models.BooleanField(null=False)
    imprint_text = models.ForeignKey(TranslatableTextgroup, related_name='+', on_delete=models.DO_NOTHING, null=True,
                                     blank=True)
    privacy_policy_text = models.ForeignKey(TranslatableTextgroup, related_name='+', on_delete=models.DO_NOTHING,
                                            null=True, blank=True)
    default_meta_description = models.OneToOneField(TranslatableSmalltext, related_name='+', on_delete=models.CASCADE,
                                                    blank=True, null=True)


class Category(models.Model):
    name = models.OneToOneField(TranslatableSmalltext, related_name='+', on_delete=models.CASCADE, blank=False,
                                null=False)

    def __str__(self):
        if len(TranslatedSmalltext.objects.filter(translatable_smalltext_id=self.name_id)) > 0:
            return TranslatedSmalltext.objects.filter(translatable_smalltext_id=self.name_id)[0].text
        else:
            return "Empty category"


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


def get_list_of_files(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles.append(fullPath)

    return allFiles


def get_attachment_path(instance, filename):
    rnd_str = random_string(42)
    while any(rnd_str in s for s in get_list_of_files(settings.MEDIA_ROOT + "/attachments/")):
        rnd_str = random_string(42)
    return 'attachments/' + rnd_str + '/' + filename


class Attachment(models.Model):
    file = models.FileField(upload_to=get_attachment_path)


class Entry(models.Model):
    categories = models.ManyToManyField(Category, related_name='entries', blank=False)
    author = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        if len(Content.objects.filter(entry_id=self.id)) > 0:
            return Content.objects.filter(entry_id=self.id)[0].title
        else:
            return "Empty entry"


class Content(models.Model):
    title = models.CharField(max_length=256, blank=False)
    summary = models.CharField(max_length=200, blank=False)
    text = RichTextField(blank=False, null=False)
    header_image = models.ForeignKey(Attachment, on_delete=models.DO_NOTHING, related_name='contents', null=True,
                                     blank=True)
    creation_date = models.DateTimeField(null=False)
    last_edit_date = models.DateTimeField(null=True, blank=True)
    # attachments = models.ManyToManyField(Attachment, related_name='contents', blank=True)
    language = models.ForeignKey(Language, null=False, on_delete=models.CASCADE, related_name='contents')
    entry = models.ForeignKey(Entry, null=False, on_delete=models.CASCADE, related_name='contents')
    tags = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author_name = models.CharField(max_length=80, null=True, blank=True)
    author_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='comments',
                                    blank=True)
    text = models.TextField(blank=False)
    passed = models.BooleanField(null=False, default=0)
    publish_date = models.DateTimeField(null=False, auto_now_add=True)
    content = models.ForeignKey(Content, null=True, on_delete=models.CASCADE, related_name='comments', blank=True)
    answer_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='answers', blank=True)

    def __str__(self):
        return self.text
