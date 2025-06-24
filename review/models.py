from django.db import models
from doctor.models import Doctor
from user.models import User
from appointment.models import Patient_appointment
# Create your models here.

RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    appointment = models.OneToOneField(Patient_appointment, on_delete=models.CASCADE,null=True,blank=True)
    review = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.doctor}/{self.rating}"
    class Meta:
        ordering = ['-created_at']
