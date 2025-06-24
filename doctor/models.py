from django.db import models
from user.models import User
from django.db.models import Avg
# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile',null=True)
    registration_no = models.CharField(max_length=20,)
    specialty = models.CharField(max_length=40)
    # degrees = models.CharField(max_length=40)
    qualification = models.CharField(max_length=200,    blank=True, null=True)
    chamber_address = models.CharField(max_length=200)
    contact = models.CharField(max_length=11)
    hospital_name = models.CharField(max_length=30)
    image_url = models.URLField(blank=True,null=True)
    experience_years = models.PositiveIntegerField(default=0)
    signature_image = models.ImageField(upload_to='doctor_signatures/', blank=True, null=True)
    description = models.TextField(null=True,blank=True)
    working_hours = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def total_review(self):
        return self.reviews.count()
    def total_rating(self):
        avg_rating = self.reviews.aggregate(avg = Avg('rating'))['avg'] or 0
        return round(avg_rating, 1)
    class Meta:
        ordering = ['-experience_years',]


APPLICACTION_STATUS = (
    ('pending', 'pending'),
    ('approved','approved'),
    ('rejected', 'rejected')
)
class DoctorApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_application')
    first_name = models.CharField(max_length=30,default=' ')
    last_name = models.CharField(max_length=20, default=' ')
    registration_no = models.CharField(max_length=20,)
    specialty = models.CharField(max_length=40)
    qualification = models.CharField(max_length=200,)
    chamber_address = models.CharField(max_length=200)
    contact = models.CharField(max_length=11)
    hospital_name = models.CharField(max_length=30)
    status = models.CharField(max_length=10 , choices=APPLICACTION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}/{self.qualification}/{self.status}"