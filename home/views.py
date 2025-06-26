from django.shortcuts import render
# Create your views here.
def home(req):
    # messages.success(req, 'HEELLOW')
    return render(req, 'home.html')