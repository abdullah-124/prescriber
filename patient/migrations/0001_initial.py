# Generated by Django 5.0.1 on 2025-05-01 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Other')], max_length=6)),
                ('address', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=11, null=True)),
                ('weight', models.PositiveIntegerField()),
            ],
        ),
    ]
