# Generated by Django 5.0.1 on 2025-05-27 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medication', '0004_remove_medication_custom_frequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='drugs',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='medication',
            name='instruction',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='medication',
            name='timing',
            field=models.CharField(max_length=20),
        ),
    ]
