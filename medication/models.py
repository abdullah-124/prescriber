from django.db import models
from precription.models import Prescription
from drugs.models import Drugs

# Create your models here.
FREQUENCY_CHOICES = [
    ('once_day', 'Once a day'),
    ('twice_day', 'Twice a day'),
    ('thrice_day', 'Thrice a day'),
    ('every_6_hours', 'Every 6 hours'),
    ('custom', 'Custom(Enter bellow)'),
]

TIMING_CHOICES = [
    ('before_meal', 'Before meal'),
    ('after_meal', 'After meal'),
    ('with_meal', 'With meal'),
    ('empty_stomach', 'On empty stomach'),
    ('custom', 'Custom(Enter bellow)'),
]
class Medication(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medication',null=True)
    drugs = models.CharField(max_length= 60)
    frequency = models.CharField(max_length=20,)
    timing = models.CharField(max_length=20, )
    instruction = models.CharField(max_length=20)