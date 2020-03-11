# Generated by Django 3.0.3 on 2020-03-11 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_auto_20200310_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='default_open_graph_image',
            field=models.FileField(blank=True, null=True, upload_to='og_image'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='favicon_ico',
            field=models.FileField(blank=True, null=True, upload_to='favicons/ico'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='favicon_png',
            field=models.FileField(blank=True, null=True, upload_to='favicons/png'),
        ),
    ]