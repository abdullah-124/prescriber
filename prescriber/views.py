from django.http import JsonResponse,HttpResponse
from django.urls import get_resolver
from django.forms.models import model_to_dict
from doctor.models import Doctor
from user.models import User
from review.models import Review
from patient.models import Patient
from appointment.models import AppointmentSession
from datetime import timedelta
from django.contrib import messages
dummy = [
    {
        "seat": 5,
        "appointment_date": "2025-06-10",
        "start_time": "09:00:00",
        "end_time": "10:00:00"
    },
    {
        "seat": 3,
        "appointment_date": "2025-06-10",
        "start_time": "10:30:00",
        "end_time": "11:30:00"
    },
    {
        "seat": 0,
        "appointment_date": "2025-06-11",
        "start_time": "14:00:00",
        "end_time": "15:00:00"
    },
    {
        "seat": 8,
        "appointment_date": "2025-06-12",
        "start_time": "08:00:00",
        "end_time": "09:30:00"
    }
]


def my_function(req):
    
    return HttpResponse('done')






# user = User.objects.create(
#             username = i.get('username'),
#             email = i.get('email'),
#             password = i.get('password'),
#             first_name = i.get('first_name'),
#             last_name = i.get('last_name'),
#             phone_number = i.get('phone_number'),
#             role = i.get('role'),
#         )
#         doctor = Doctor.objects.create(
#             user= user,
#             registration_no = i.get('registration_no'),
#             specialty = i.get('specialty'),
#             qualification = i.get('qualification'),
#             chamber_address = i.get('chamber_address'),
#             contact = i.get('contact'),
#             hospital_name = i.get('hospital_name'),
#             experience_years = i.get('experience_years'),
#             description = i.get('description'),
#             working_hours = i.get('working_hours'),

#         )
#         print(doctor.user)