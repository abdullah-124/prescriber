# Generated by Django 5.0.1 on 2025-04-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drugs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=50)),
                ('generic', models.TextField()),
                ('strength', models.TextField(max_length=100)),
                ('dosage', models.TextField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('use_for', models.CharField(max_length=12)),
                ('DAR', models.IntegerField()),
            ],
        ),
    ]
