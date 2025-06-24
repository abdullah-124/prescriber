from django.shortcuts import render, get_object_or_404
from appointment.models import Patient_appointment
from precription.models import Prescription
from django.http import JsonResponse


# Create your views here.
def get_medicines_list(req,id):
    appointment = get_object_or_404(Patient_appointment, id=id)
    prescription = Prescription.objects.filter(appointment=appointment)
    if(prescription.exists()):
        medicines = prescription.first().medication.all().values('drugs','frequency','timing','instruction')
        print('get medicines')
        return JsonResponse(list(medicines),status=200,safe=False)
    return JsonResponse([], status=201,safe=False)