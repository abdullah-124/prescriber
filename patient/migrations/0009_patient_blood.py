# Generated by Django 5.0.1 on 2025-06-11 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0008_alter_patient_height'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='blood',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], default='A+', max_length=3),
        ),
    ]
