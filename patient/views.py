from django.shortcuts import render,get_object_or_404,HttpResponse, redirect
from django.urls import reverse_lazy
from django.db.models import Case, When, IntegerField
from django.views import View
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from appointment.models import Patient_appointment
from doctor.decorators import doctor_required
from patient.forms import PatientForm_doctor_view, PatientUpdateForm,PatientCreateForm
from django.contrib import messages
from patient.models import Patient
from datetime import date
# Create your views here.
@doctor_required
def patient_profile(req, id):
    p_appointment = get_object_or_404(Patient_appointment,id = id)
    if(p_appointment.session.doctor.user != req.user ):
        return HttpResponse('<h3>502 bad request</h3>')
    p_appointment.status = 'Running'
    p_appointment.save()
    patient = p_appointment.patient
    previous_appointments = Patient_appointment.objects.filter(patient = patient,status='Seen').exclude(id = p_appointment.id).order_by('-created_at')
    if req.method == 'POST':
        # print('post')
        form = PatientForm_doctor_view(req.POST, instance=patient)
        if(form.is_valid()):  
            updated_patient = form.save()
            reason =  req.POST.get('reason')
            p_appointment.reason = reason
            p_appointment.save()  
            messages.success(req, "Updated")
            # print('updatedd')
            return redirect('patient_profile_doctor_view',p_appointment.id)
        else:
            messages.error(req,form.errors)
    else : 
        form = PatientForm_doctor_view(instance=patient)
    
    context = {
        'form': form,
        'patient': patient,
        'appointment': p_appointment,
        'previous_appointments': previous_appointments,
    }
    return render(req, 'patient_profile.html', context)

class Patient_profile_User_view(LoginRequiredMixin, View):
    template_name = 'patient_profile_user_view.html'
    def get(self,request,id):
        patient = get_object_or_404(Patient, id=id)
        if(patient.creator != request.user):
            return HttpResponse('<h1>Page not found 502</h1>')
        #  main task
        form = PatientUpdateForm(instance=patient)
        previous_appointments = Patient_appointment.objects.filter(patient = patient,status='Seen').order_by('-created_at')
        appointments =  Patient_appointment.objects.filter(patient = patient, session__appointment_date__gt = date.today())
        context = {
            'form': form,
            'patient': patient,
            'appointments': appointments,
            'previous_appointments' : previous_appointments,
        }
        return render(request, self.template_name, context)
    def post(self, request,id):
        patient = get_object_or_404(Patient, id = id)
        if(patient.creator != request.user):
            return HttpResponse('<h1>Page not found</h1>')
        form = PatientUpdateForm(request.POST, instance=patient)
        # validation
        if(form.is_valid()):
            form.save()
            messages.success(request, "Updated")
            return redirect('patient_profile_user_view',patient.id)
        else :
            messages.error(request, form.errors)

        previous_appointments = Patient_appointment.objects.filter(patient = patient,status='Seen').order_by('-created_at')
        context = {
            'form': form,
            'patient': patient,
            'previous_appointments' : previous_appointments
        }
        return render(request, self.template_name, context)
    
# My patient list it returns all patients were created by req.user
class MyPatient(LoginRequiredMixin,View):
    template_name = 'my_patients.html'
    def get(self, request):
        data = request.user.my_patients.all()
        patients = data.annotate(
            priority = Case(
                When(label='Other', then=0),
                When(label = 'you',then=3),
                When(label = 'mother', then=2),
                When(label = 'father', then=2),
                default= 1,
                output_field=IntegerField()
            )
        ).order_by('-priority','last_updated')
        form = PatientCreateForm()
        return render(request, self.template_name, {'patients':patients, 'form':form})
    # 
    def post(self,request):
        form  = PatientCreateForm(request.POST)
        if(form.is_valid()):
            # print('bla bla bla...')
            # print(form.cleaned_data)
            patient = form.save(commit=False)
            patient.creator = request.user
            patient.save()
            messages.success(request, "✅ Patient has created")
        else :
            messages.error(request, form.errors)
        return redirect('my_patients')
    


class Patient_delete(DeleteView):
    model = Patient
    success_url = reverse_lazy('my_patients')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.creator != request.user:
            return HttpResponse('Bad request 502')
        messages.success(request, f"Patient '{obj.name}' deleted successfully.")
        return super().delete(request, *args, **kwargs)