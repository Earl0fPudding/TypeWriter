# Generated by Django 3.0.3 on 2020-03-11 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20200311_0629'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='socket',
            field=models.CharField(default='http://localhost:8000', max_length=100),
            preserve_default=False,
        ),
    ]