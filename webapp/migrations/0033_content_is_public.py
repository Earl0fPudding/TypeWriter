# Generated by Django 3.0.3 on 2020-03-26 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0032_settings_socket'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
