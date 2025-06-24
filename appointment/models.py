from django.db import models
from doctor.models import Doctor
from user.models import User
from patient.models import Patient
from appointment.manager import AppointmentSessionManager
from django.utils import timezone


# MODELS
class AppointmentSession(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='sessions')
    seat = models.IntegerField(default=0)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AppointmentSessionManager()
    def __str__(self):
        return f"{self.doctor}/{self.appointment_date}/{self.start_time}"
    def total_booking(self):
        total = self.bookings.count()
        return total
    def is_available(self):
        return self.seat > self.bookings.count()
    
    class Meta: 
        ordering = ['doctor','appointment_date', 'start_time']
    
    
    
# APPOINTMENT BOOKING FOR PATIENT
APPOINTMENT_STATUS = (
        ('Seen', 'Seen'),
        ('Queue', 'Queue'),
        ('Running', 'Running'),
        ('Missing', 'Missing'),
    )
class Patient_appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    session = models.ForeignKey(AppointmentSession, on_delete=models.CASCADE, related_name='bookings' )
    reason = models.TextField(null=True, blank=True)
    diagnosis = models.CharField(max_length=50, null=True, blank=True)
    status = models.TextField(max_length=10, choices=APPOINTMENT_STATUS ,default='Queue')
    serial_no = models.PositiveIntegerField(null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        unique_together = ('patient', 'session')
    class Meta :
        ordering = ['-created_at','serial_no']
    def __str__(self):
        return f"{self.patient}/{self.session}"