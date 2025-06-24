from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

ROLE_CHOICES = (
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    )
class User(AbstractUser):
    role = models.CharField(max_length=10, default='patient', choices=ROLE_CHOICES)
    points = models.PositiveIntegerField(default=1)
    phone_number = models.CharField(max_length=11)
    photo = models.ImageField(upload_to='user/', blank=True,null=True)
    
    # 
    def is_doctor(self):
        return self.role == 'doctor'
    def is_patient(self):
        return self.role == 'patient'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"