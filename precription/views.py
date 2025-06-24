from django.shortcuts import render, get_object_or_404,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from appointment.models import Patient_appointment
from precription.forms import PrescriptionForm
from doctor.decorators import doctor_required, DoctorRequiredMixin
from precription.models import Prescription
from medication.models import Medication
from medication.sub_function import handle_medicine
from doctor.models import Doctor
import json
import json
# Create your views here.
@doctor_required
def make_prescription(req, id):
    appointment = get_object_or_404(Patient_appointment, id = id)
    doctor = get_object_or_404(Doctor, user = req.user)
    patient = appointment.patient
    if(appointment.session.doctor != doctor):
        return HttpResponse('<h3>502 bad request</h3>')
    if(req.method == 'POST'):
        form = PrescriptionForm(req.POST)
        json_medicines = req.POST.get('medicines')
        diagnosis = req.POST.get('diagnosis')
        if(form.is_valid() and json_medicines):
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            medicines = json.loads(json_medicines)
            for m in medicines:
                if(m.get('status')):
                    handle_medicine(m, prescription_id=prescription.id)
            appointment.status = 'Seen'
            appointment.diagnosis = diagnosis
            appointment.save()
            return redirect('get_prescription',appointment.id)
        else : 
            messages.info(req, "Provide Proper information")
    else :
        form = PrescriptionForm()
    context = {
        'appointment': appointment,
        'patient': patient,
        'doctor': doctor,
        'form': form,
    }
    return render(req, 'prescription_form.html', context)



class PrescriptionUpdate_View(View):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescription_update.html'
    def get(self,request, id):
        appointment = get_object_or_404(Patient_appointment,id=id)
        doctor = appointment.session.doctor
        patient = appointment.patient
        if doctor.user != request.user:
            return HttpResponse('<h1>Bad request</h1>')
        prescription = get_object_or_404(Prescription, appointment=appointment)
        medications = prescription.medication.all().values()
        # print('this is ',medications)
        form = PrescriptionForm(instance=prescription)
        context = {
            'doctor': doctor,
            'patient': patient,
            'medications':json.dumps(list(medications)),
            'appointment': appointment,
            'form': form,
        }
        return render(request, self.template_name, context)
    def post(self,request,id):
        appointment = get_object_or_404(Patient_appointment,id=id)
        if(appointment.session.doctor.user != request.user):
            return HttpResponse('<h1>BAD REQUEST</h1>')
        prescription = get_object_or_404(Prescription, appointment=appointment)
        medications = prescription.medication.all().values()
        form = PrescriptionForm(request.POST, instance=prescription)
        json_medicines = request.POST.get('json_medicines')
        if form.is_valid():
            # print('hellow', form.cleaned_data)
            form.save()
            medicines = json.loads(json_medicines)
            for m in medicines: 
                # print('########  this is------------', m)
                if(m.get('status')):
                    res = handle_medicine(m, prescription_id=prescription.id)
                    print(res)
            return redirect('get_prescription', appointment.id)
                
                
            
        context = {
            'appointment': appointment,
            'patient': appointment.patient,
            'doctor': appointment.session.doctor,
            'medications':json.dumps(list(medications)),
            'form': form,
        }
        return render(request, self.template_name, context)


class Prescription_User_View(View):
    def get(self, request, id):
        appointment = Patient_appointment.objects.get(id=id)
        prescription = appointment.prescription
        medications = prescription.medication.all()
        # print(medications)
        
        context = {
            'doctor': appointment.session.doctor,
            'rx': prescription,
            'patient': prescription.appointment.patient,
            'appointment': appointment,
            'medications': medications,
        }
        return render(request, 'prescription_user_view.html', context=context)
    
def demo_prescription(req):
    return render(req, 'demo_prescription.html')