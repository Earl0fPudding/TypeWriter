# Generated by Django 2.2.9 on 2019-12-28 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20191228_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='original_filename',
        ),
    ]
