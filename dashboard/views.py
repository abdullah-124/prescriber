from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from doctor.decorators import doctor_required
from appointment.forms import AppoiontmentSessionForm
from appointment.models import AppointmentSession, Patient_appointment
from doctor.models import Doctor
# Create your views here.
@doctor_required
def overview(req):
    doctor = get_object_or_404(Doctor, user = req.user)
    now = timezone.now()
    bookings = Patient_appointment.objects.filter(session__doctor = doctor)
    sessions = AppointmentSession.objects.filter( doctor=doctor)
    total_bookings = bookings.count()
    total_patients = bookings.values('patient').distinct().count()
    running_sessions = AppointmentSession.objects.is_running().filter(doctor=doctor)
    running_patients = []
    if running_sessions:
        running_patients = running_sessions[0].bookings.all().filter(status='Queue')
    appointment_request = bookings.filter(
        session__appointment_date__gte = now.date(), 
    ).exclude(
        session__appointment_date__lt = now.date(),
        session__start_time__lte = now.time(),
        session__end_time__gte = now.time()
    )[:5]
    context = {
        'total_sessions': sessions.count(),
        'total_bookings': total_bookings,
        'total_patients': total_patients,
        'total_reviews': doctor.total_review,
        'total_rating': doctor.total_rating,
        'running_patients' : running_patients,
        'appointment_request': appointment_request,
    }
    return render(req, 'dashboard/overview.html', context)

