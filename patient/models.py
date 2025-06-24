from django.db import models
from user.models import User
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
GENDER = [
    ('Male', 'M'),
    ('Female', 'F'),
    ('Other', 'N')
]

BLOOD_GROUP = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

class Patient(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_patients')
    label = models.CharField(max_length=20, default='Other')
    name = models.CharField(max_length=30)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=6, choices=GENDER)
    mobile = PhoneNumberField(region = 'BD')
    address = models.CharField(max_length=100, null=True, blank=True)
    bp = models.CharField(null=True,blank=True, max_length=8)
    weight = models.PositiveIntegerField(null=True,blank=True)
    height = models.PositiveIntegerField(null=True,blank=True)
    blood = models.CharField(max_length=3, choices=BLOOD_GROUP, default='A+')
    temperature = models.DecimalField(decimal_places=1, max_digits=3,null=True,blank=True)
    bg_after = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    bg_before = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    last_updated = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}/{self.dob}"
    @property
    def age(self):
        today = date.today()
        dob = self.dob
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))