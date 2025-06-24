from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User
class UserRegestrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'value': 'Test@1234'
        })  
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'value': 'Test@1234'
        })  
    )
    class Meta: 
        model = User
        fields = ['first_name','last_name','email','username','phone_number','password1','password2']



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','phone_number','photo']

