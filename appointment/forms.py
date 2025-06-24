from django import forms
from appointment.models import AppointmentSession, Patient_appointment
from patient.models import Patient


class AppoiontmentSessionForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': '02:30 PM','type':'time'}),

    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': '02:30 PM','type':'time'}),

    )
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs= {'placeholder':'YYYY-DD-MM','type':'date'})
    )
    class Meta:
        model = AppointmentSession
        fields = ['seat','appointment_date', 'start_time', 'end_time']
        
class AppointmentBookingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'autocomplete': 'off',
        'placeholder': 'Enter patient name'
    }))
    mobile = forms.CharField(max_length=14)
    dob = forms.DateField(label='Date of Birth')
    class Meta: 
        model = Patient_appointment
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Reason for taking appointment'
            })
        }
        
    