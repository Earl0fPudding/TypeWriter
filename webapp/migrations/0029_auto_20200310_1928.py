# Generated by Django 3.0.3 on 2020-03-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_auto_20200310_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='default_meta_description',
        ),
        migrations.AddField(
            model_name='settings',
            name='favicon_png',
            field=models.FileField(blank=True, null=True, upload_to='favicon.png'),
        ),
    ]
