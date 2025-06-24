from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def home(req):
    # messages.success(req, 'HEELLOW')
    return render(req, 'home.html')