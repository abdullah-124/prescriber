from django.contrib import admin
from appointment.models import AppointmentSession, Patient_appointment
# Register your models here.
@admin.register(AppointmentSession)
class AppointmentSession(admin.ModelAdmin):
    list_display = [field.name for field in AppointmentSession._meta.fields]
    # list_display = ['doctor','start_time']
    
@admin.register(Patient_appointment)
class PatientAppointmentSession(admin.ModelAdmin):
    list_display = [field.name for field in Patient_appointment._meta.fields]