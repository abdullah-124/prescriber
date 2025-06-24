from django.contrib import admin
from precription.models import Prescription
# Register your models here.

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Prescription._meta.fields]