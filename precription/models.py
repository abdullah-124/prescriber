from django.db import models
from appointment.models import Patient_appointment
# Create your models here.
class Prescription(models.Model):
    appointment = models.OneToOneField(Patient_appointment, on_delete=models.CASCADE, related_name='prescription')
    instruction = models.TextField(null=True,blank=True)
    examination = models.TextField(null=True, blank=True)
    diagnosis = models.CharField(max_length=50, null=True, blank=True)
    bp = models.CharField(null=True,blank=True, max_length=8)
    weight = models.PositiveIntegerField(null=True,blank=True)
    height = models.PositiveIntegerField(null=True,blank=True)
    blood = models.CharField(max_length=3,default='A+')
    temperature = models.DecimalField(decimal_places=1, max_digits=3,null=True,blank=True)
    bg_after = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    bg_before = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.appointment}"
    def save(self, *args, **kwargs):
        patient = self.appointment.patient
        self.bp = patient.bp
        self.weight = patient.weight
        self.height = patient.height
        self.blood = patient.blood
        self.temperature = patient.temperature
        self.bg_after = patient.bg_after
        self.bg_before = patient.bg_before
        super().save(*args, **kwargs)