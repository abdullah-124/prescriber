from django.contrib import admin
from medication.models import Medication
# Register your models here.
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Medication._meta.fields]