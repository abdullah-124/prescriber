from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.


now = timezone.localtime()
time = now + timedelta(hours=6)
current_time = time.time()
class AppointmentSessionManager(models.Manager):
    def is_ongoing(self):
        return self.get_queryset().filter(appointment_date__gte = now.date(), end_time__gte=current_time)
    def is_running(self):
        return self.get_queryset().filter(appointment_date = now.date(), start_time__lte=current_time, end_time__gte=current_time)
    def todays(self):
        return self.get_queryset().filter(appointment_date = now.today())