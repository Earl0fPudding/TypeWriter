# Generated by Django 3.0.3 on 2020-02-18 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0022_auto_20200218_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='webapp.TranslatableSmalltext', unique=True),
        ),
    ]
