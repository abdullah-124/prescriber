from django import forms
from review.models import Review

class Patient_review_form(forms.ModelForm):
    review = forms.CharField(max_length=200, required=False,
    widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder':'Share your experience'}, )                         
    )
    class Meta: 
        model = Review
        fields = ['review','rating']