from review.models import Review
from django.contrib import messages
from review.forms import Patient_review_form
from appointment.models import Patient_appointment
from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def patient_review(request,id):
    print(id)
    # try:
    appointment = Patient_appointment.objects.get(id=id,patient__creator = request.user)
    reviews = Review.objects.filter(appointment=appointment)
    if request.method == 'POST':
        form = Patient_review_form(request.POST)
        if(reviews.exists):
            form = Patient_review_form(request.POST, instance=reviews.first())
        if(form.is_valid()):
            review = form.save(commit=False)
            review.appointment = appointment
            review.doctor = appointment.session.doctor
            review.save()
            messages.success(request,'✅ review has posted.')
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, form.errors)
    else :
        if reviews.exists():
            form = Patient_review_form(instance=reviews.first())
        else:
            form = Patient_review_form()
        
    # except:
    #     return HttpResponse('<h1>Bad request 502 </h1>')
    return render(request, 'review_form.html', {'form':form})