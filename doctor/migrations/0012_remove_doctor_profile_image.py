# Generated by Django 5.0.1 on 2025-06-01 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0011_alter_doctor_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='profile_image',
        ),
    ]
