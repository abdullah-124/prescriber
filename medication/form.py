from django.forms import inlineformset_factory, ModelForm
from precription.models import Prescription
from medication.models import Medication


class MedicationForm(ModelForm):
    class Meta: 
        model = Medication
        fields = ['drugs','frequency','timing','instruction']

