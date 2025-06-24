from django import forms
from precription.models import Prescription

class PrescriptionForm(forms.ModelForm):
    examination = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder':'Examination'}, )
    )
    instruction = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder':'Instruction', })
    )
    
    class Meta: 
        model = Prescription
        fields = ['instruction','examination','diagnosis']