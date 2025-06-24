from django import forms
from patient.models import Patient
from phonenumber_field.formfields import PhoneNumberField


class PatientForm_doctor_view(forms.ModelForm):
    class Meta :
        model = Patient
        fields = ['height','weight','bp','temperature','bg_after','bg_before']
        labels = {
            'dob': 'Date of Birth',
            'bg_after': '<span class="text-[10px]">Blood Glucose After Meal</span>',
            'bg_before': '<span class="text-[10px]">Blood Glucose Before Meal</span>',
            'bp' : 'Blood Pressure',
            
        }

class PatientUpdateForm(forms.ModelForm):
    mobile = PhoneNumberField(
        region='BD',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200',
            'placeholder': '+8801XXXXXXXXX'
        })
    )
    class Meta :
        model = Patient
        fields = "__all__"
        exclude = ['creator']
        labels = {
            'dob': 'Date of Birth',
            'bg_after': '<span class="text-[10px]">Blood Glucose After Meal</span>',
            'bg_before': '<span class="text-[10px]">Blood Glucose Before Meal</span>',
            'bp' : 'Blood Pressure',
            
        }
class PatientCreateForm(forms.ModelForm):
    class Meta: 
        model = Patient
        fields = ['name', 'label','dob','address','gender','mobile']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }