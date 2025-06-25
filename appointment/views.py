from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models.functions import Concat
from django.db.models import Value,TextField
from django.contrib.auth.decorators import login_required
from appointment.models import AppointmentSession,Patient_appointment
from appointment.forms import AppoiontmentSessionForm
from patient.models import Patient
from doctor.models import Doctor
from doctor.decorators import DoctorRequiredMixin
from appointment.forms import AppointmentBookingForm
import json


now = timezone.now()

# list,booking
class Appointment(LoginRequiredMixin,View):
    template_name = 'appointment.html'
    def get(self, request, status = None, pk=None):
        try:
            if(status == 'booking'):
                session = get_object_or_404(AppointmentSession, id = pk)
                form = AppointmentBookingForm()
                data = request.user.my_patients.all().values('name','mobile','dob','label')
                my_patients = json.dumps(list(data), default=str)
                context = {
                    'patient_form': form,
                    'session': session,
                    'doctor' : session.doctor,
                    'my_patients': my_patients  
                }
                return render(request, 'booking.html',context)
            elif status == 'patient_list':
                session = get_object_or_404(AppointmentSession, id = pk)
                bookings = session.bookings.all().order_by('serial_no')
                context = {
                    'bookings': bookings,
                    'session': session
                }
                return render(request, 'appointment_status.html', context)
            # my appointments
            elif(status == 'my_appointments'):
                q = request.GET.get('q')
                appointments = Patient_appointment.objects.filter(patient__creator = request.user)
                if(q == 'past'):
                    appointments = appointments.filter(session__appointment_date__lt = now.today())
                else: 
                    appointments = appointments.filter(session__appointment_date__gte = now.today())
                
                paginator = Paginator(appointments, 6)
                page_num = request.GET.get('page')
                my_appointments = paginator.get_page(page_num)
                patients = request.user.my_patients.all()
                # print(patients)
                context =  {
                    'q':q, 
                    'patients':patients,
                    'appointments':my_appointments,
                }
                return render(request, 'my_appointment.html',context)
            
            # else all appointments are sended
            result = AppointmentSession.objects.filter(appointment_date__gte = now.today()).order_by('appointment_date','start_time')
            paginator = Paginator(result,12)
            page_num = request.GET.get('page')
            sessions = paginator.get_page(page_num)
            context = {
                'sessions': sessions,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(request, e)
            return render(request, 'not_found.html')
        
    def post(self,request, status=None, pk = None):
        try:
            if status == 'booking':
                session = get_object_or_404(AppointmentSession, id = pk)
                form = AppointmentBookingForm(request.POST)
                data = request.user.my_patients.all().values('name','mobile','dob','label')
                my_patients = json.dumps(list(data), default=str)
                if(form.is_valid()):
                    print(form.cleaned_data)
                    
                    name = form.cleaned_data['name']
                    mobile = form.cleaned_data['mobile']
                    dob = form.cleaned_data['dob']
                    patients = Patient.objects.filter(name=name,mobile=mobile,dob=dob)
                    if(not patients.exists()):
                        patient = Patient.objects.create(
                            creator=request.user, name = name,mobile = mobile,dob = dob
                        )
                    else: 
                        patient = patients.first()
                    isBooked = session.bookings.all().filter(patient=patient)
                    
                    if isBooked:
                        messages.warning(request,f'Already booked an appointment')
                    elif session.is_available():
                        appointment = form.save(commit=False)
                        appointment.patient = patient
                        appointment.session = session
                        appointment.serial_no = session.total_booking() + 1
                        appointment.save()
                        messages.success(request, f'Your appointment serial is {appointment.serial_no}', )
                        return redirect('patient_list',session.id)
                    else : 
                        messages.warning(request, "There is no seat available")
                else: 
                    messages.error(request, form.errors)
                context = {
                    'patient_form': form,
                    'my_patients': my_patients,
                    'session': session,
                    'doctor' : session.doctor,
                }
                return render(request, 'booking.html',context)
            return HttpResponse('something wrong...')
        except Exception as e:
            messages.error(request, e)
            return render(request, 'not_found.html')

# Searching appointment
def search_appointment(request):
    try:
        q = request.GET.get('q', '').strip().lower()
        print(q)
        if not q :
            return render(request, 'appointment.html')
        result = AppointmentSession.objects.is_ongoing().annotate(
            combined = Concat(
                'appointment_date', Value(' '),
                'doctor__user__first_name',Value(' '),
                'doctor__user__last_name',Value(' '),
                'doctor__hospital_name',Value(' '),
                'doctor__chamber_address',Value(' '),
                'doctor__specialty',
                output_field=TextField()
            )
        )
        keywords = q.split(' ')
        for k in keywords: 
            # print(k)
            result = result.filter(combined__icontains = k)
        paginator = Paginator(result, 15)
        page_num = request.GET.get('page')
        sessions = paginator.get_page(page_num)
        
        return render(request, 'appointment.html',{'sessions':sessions})
    except Exception as e: 
        messages.warning(request, e)
        return render(request, 'appointment.html',{'sessions':{}})

# DASHBOARRD view 

class Session(DoctorRequiredMixin, View):
    template_name = 'dashboard/appointment.html'
    form = None
    def get(self,request, action = None,pk=None):
        try:
            if(action=='get'):
                session = get_object_or_404(AppointmentSession, id = pk, doctor__user = request.user)
                patients = session.bookings.all().order_by('serial_no')
                context = {
                    'patients': patients,
                    'session': session
                }
                return render(request, 'dashboard/patients_list.html', context)
                
            if(action=='add'):
                form = AppoiontmentSessionForm()
            elif action == 'edit':
                session = get_object_or_404(AppointmentSession, id = pk)
                form = AppoiontmentSessionForm(instance = session)
            
            # return all appointments 
            elif action == 'all':
                q = request.GET.get('q')
                print(q)
                doctor = get_object_or_404(Doctor, user=request.user)
                data = doctor.sessions.all().order_by('-appointment_date')
                if(q):
                    data = data.filter(appointment_date = q)
                paginator = Paginator(data, 10)
                page_num = request.GET.get('page')
                sessions = paginator.get_page(page_num)
                return render(request, 'dashboard/all_appointments.html', {'sessions':sessions})  

            else :
                doctor = get_object_or_404(Doctor, user = request.user)
                # sessions = AppointmentSession.objects.is_ongoing().filter(doctor=doctor).exclude(appointment_date = now.today())
                sessions = doctor.sessions.all().filter(appointment_date__gt = now.date())
                running_sessions = AppointmentSession.objects.is_running().filter(doctor= doctor)
                todays_sessions = AppointmentSession.objects.todays().filter(doctor=doctor).exclude(id__in = running_sessions.values_list('id',flat=True))
                context = {
                    'sessions' : sessions,
                    'todays_sessions' : todays_sessions,
                    'running_sessions' : running_sessions
                }
                return render(request, 'dashboard/appointment_list.html', context)
            return render(request, self.template_name, {'form':form, 'action':action})
        except Exception as e:
            messages.error(request, e)
            return render(request, 'not_found.html')
    # POST 
    def post(self,request, action, pk=None):
        try:
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
                    print('Is overloap', has_overlap)
                    if not has_overlap:
                        session.save()
                        messages.success(request, 'Appointment created.')
                        return render(request, self.template_name, {'form':form})
                    else :
                        messages.error(request, "There has an another session in this timeslot")
                else:
                    messages.error(request, form.errors)
            elif action == 'edit':
                session = get_object_or_404(AppointmentSession, id = pk)
                form = AppoiontmentSessionForm(request.POST, instance=session)
                
                if(form.is_valid()):
                    updated_session = form.save(commit=False)
                    has_overlap = AppointmentSession.objects.filter(
                        doctor = updated_session.doctor,
                        appointment_date = updated_session.appointment_date,
                        start_time__lt = updated_session.end_time,
                        end_time__gt = updated_session.start_time,
                    ).exclude(pk = session.pk)
                    print(has_overlap)
                    if(has_overlap):
                        messages.warning(request, "Session time has overlaped.")
                    else: 
                        form.save()
                        messages.success(request, 'UPDATED')   
                        return redirect('dashboard_appointment_list') 
                else:
                    messages.error(request, form.errors)    

            
            
            return render(request, self.template_name, {'form':form, 'action':action})
        except Exception as e:
            messages.error(request, e)
            return render(request, 'not_found.html')


class Add_patient(DoctorRequiredMixin, View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            session_id = int(data['session'])
            # print(type(session_id))
            
            session = get_object_or_404(AppointmentSession, id = session_id, doctor__user = request.user)
            # return JsonResponse(str(session), safe=False)
            if not session.is_available:
                return JsonResponse({'message':'There is no available seat'},status=409)
            
            patient = Patient.objects.filter(name=data['name'], dob=data['dob'], mobile=data['mobile'])
            print(patient)
            if not patient:
                print('created')
                patient = Patient.objects.create(
                    creator= request.user,
                    name = data['name'],
                    dob = data['dob'],
                    mobile = data['mobile']
                )
            else :
                patient = patient.first()
            print(patient)
            
            is_booked = session.bookings.all().filter(patient=patient)
            if(is_booked.exists()):
                return JsonResponse({'message':'Alredy booked an appointment'},status=409)
            elif session.is_available:
                appointment = Patient_appointment.objects.create(
                    patient = patient,
                    session = session,
                    serial_no = session.total_booking() + 1
                )
                return JsonResponse({'message':f'Appointment serial is {appointment.serial_no}'},status=202)
            return JsonResponse({'message':'Some thing went wrong'},status=409)
        except:
            return render(request, 'not_found.html')

