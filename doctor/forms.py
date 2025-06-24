from django import forms 
from doctor.models import Doctor, DoctorApplication

class DoctorPortfolioForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['registration_no','specialty','qualification','chamber_address','contact','hospital_name','experience_years','description','working_hours', ]

class DoctorProfileUpdate(forms.ModelForm):
    class Meta: 
        model = Doctor
        fields = '__all__'
        exclude = ['user']
        
class Doctor_applicatioin_form(forms.ModelForm):
    class Meta: 
        model = DoctorApplication
        fields = '__all__'
        exclude = ['user','status']