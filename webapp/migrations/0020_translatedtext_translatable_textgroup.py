# Generated by Django 3.0.2 on 2020-01-15 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_translatedtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='translatedtext',
            name='translatable_textgroup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='translated_texts', to='webapp.TranslatableTextgroup'),
            preserve_default=False,
        ),
    ]