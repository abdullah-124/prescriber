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
    todays_session = AppointmentSession.objects.is_running().filter(doctor=doctor)
    running_patients = []
    if todays_session:
        running_patients = todays_session[0].bookings.all().filter(status='Queue')
    appointment_request = bookings.filter(
        session__appointment_date__gte = now.date(), 
    ).exclude(
        session__appointment_date__gte = now.date(),
        session__start_time__lte = now.time(),
        session__end_time__gte = now.time()
    )
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

@doctor_required
def appointment(req):
    if req.method == 'POST':
        form = AppoiontmentSessionForm(req.POST)
        # if(not req.user.is_doctor):
        #     return 
        if(form.is_valid()):
            print(form.cleaned_data)
            session = form.save(commit=False)
            doctor = Doctor.objects.get(user = req.user)
            session.doctor = doctor
            has_overlap = AppointmentSession.objects.filter(
                doctor = session.doctor,
                appointment_date = session.appointment_date,
                start_time__lt = session.end_time,
                end_time__gt = session.start_time,
            ).exists()
            print('sdfsfdff', has_overlap)
            if not has_overlap:
                session.save()
                messages.success(req, 'Appointment created.')
                return render(req, 'dashboard/appointment.html', {'form':form})
            else :
                messages.error(req, "There has another appointment session at this time.")
        else:
            messages.error(req, form.errors)
    
    else :
        form = AppoiontmentSessionForm()
    return render(req, 'dashboard/create_appointment.html', {'form':form})
# create view 
class Session(View):
    template_name = 'dashboard/appointment.html'
    form = None
    def get(self,request, action = None,pk=None):
        if(action=='get'):
            session = get_object_or_404(AppointmentSession, id = pk)
            patients = session.bookings.all().order_by('serial_no')
            context = {
                'patients': patients
            }
            return render(request, 'patient/patient.html', context)
            
        if(action=='add'):
            form = AppoiontmentSessionForm()
        elif action == 'edit':
            session = get_object_or_404(AppointmentSession, id = pk)
            form = AppoiontmentSessionForm(instance = session)
        else :
            doctor = get_object_or_404(Doctor, user = request.user)
            sessions = AppointmentSession.objects.is_ongoing().filter(doctor=doctor)
            context = {
                'sessions' : sessions
            }
            return render(request, 'dashboard/appointment_list.html', context)
        return render(request, self.template_name, {'form':form, 'action':action})
    # POST 
    def post(self,request, action, pk=None):
        if(action=='add'):
            form =  AppoiontmentSessionForm(request.POST)
            if(form.is_valid()):
                session = form.save(commit=False)
                doctor = Doctor.objects.get(user = request.user)
                session.doctor = doctor
                has_overlap = AppointmentSession.objects.filter(
                    doctor = session.doctor,
                    appointment_date = session.appointment_date,
                    start_time__lt = session.end_time,
                    end_time__gt = session.start_time,
                ).exists()
                print('is overloap', has_overlap)
                if not has_overlap:
                    # session.save()
                    messages.success(request, 'Appointment created.')
                    # return render(request, self.template_name, {'form':form})
                else :
                    messages.error(request, "There has an another session in this timeslot")
            else:
                messages.error(request, form.errors)
        
        return render(request, self.template_name, {'form':form, 'action':action})
                

# Appointment List

@doctor_required
def patient_list(req,id):
    session = get_object_or_404(AppointmentSession, id = id)
    patients = session.bookings.all().order_by('serial_no')
    context = {
        'patients': patients
    }
    return render(req, 'patient/patient.html', context)