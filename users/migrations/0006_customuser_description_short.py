# Generated by Django 2.2.9 on 2020-01-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191228_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description_short',
            field=models.TextField(blank=True, null=True),
        ),
    ]