# Generated by Django 3.0.3 on 2020-03-31 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0034_entry_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='token',
            field=models.CharField(default='000000', max_length=6, unique=True),
        ),
    ]
