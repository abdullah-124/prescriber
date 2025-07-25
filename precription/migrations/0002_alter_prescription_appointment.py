# Generated by Django 5.0.1 on 2025-06-11 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0020_alter_appointmentsession_options'),
        ('precription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='appointment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointment', to='appointment.patient_appointment'),
        ),
    ]
