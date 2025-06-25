from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q
from doctor.forms import DoctorProfileUpdate, Doctor_applicatioin_form
from django.contrib.auth.forms import PasswordChangeForm
from doctor.decorators import DoctorRequiredMixin
from user.forms import UserUpdateForm
from doctor.models import Doctor, DoctorApplication
from review.models import Review

# Create your views here.
@login_required
def doctor_regestration(req):
    application = DoctorApplication.objects.filter(user = req.user)
    form = Doctor_applicatioin_form()
    if(application):
        print(application.first())
        return render(req, 'account/registration.html', {'application':application.first()})
    if(req.method == 'POST'):
        form = Doctor_applicatioin_form(req.POST)
        if(form.is_valid()):
            user = req.user
            doctor_application = form.save(commit=False)
            doctor_application.user = user
            doctor_application.save()
            messages.success(req,"Your application has submitted successfuly.")
            return redirect('doctor_registration')
        else:
            messages.error(req, form.errors) 
    
    return render(req, 'account/registration.html', {'form':form,'application':None})

# doctor profile for dashboard
class Doctor_profile(DoctorRequiredMixin, View ):
    template_name = 'dashboard/doctor_profile.html'
    
    def get(self, request, status=None):
        doctor = get_object_or_404(Doctor, user__username=request.user.username)
        doctor_form = DoctorProfileUpdate(instance=doctor)
        
        password_change_form = PasswordChangeForm(user=request.user)
        reviews = doctor.reviews.all()
        context = {
            'doctor': doctor ,
            'status': status,
            'reviews': reviews,
            'doctor_form': doctor_form,
            'password_change_form': password_change_form,
        }
        return render(request, self.template_name, context )
    def post(self,request, status=None):
        doctor = get_object_or_404(Doctor, user__username=request.user.username)
        doctor_form = DoctorProfileUpdate(request.POST, request.FILES, instance=doctor)
        password_change_form = PasswordChangeForm(request.user, data=request.POST)
        if(status == 'edit_profile'):
            if(doctor_form.is_valid()):
                doctor_form.save()
                status = None
                print('hello')
                messages.success(request, 'Updated')
                return redirect('doctor_profile')
            else: 
                messages.error(request, doctor_form.errors)
        elif(status == 'change_password'):
            if(password_change_form.is_valid()):
                # print(password_change_form.cleaned_data)
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password Changed')
                return redirect('doctor_profile')
            else :
                messages.error(request, password_change_form.errors)

        context = {
            'doctor': doctor ,
            'status': status,
            'doctor_form': doctor_form,
            'password_change_form': password_change_form
        }
        return render(request, self.template_name, context )


class DoctorView(View):
    def get(self, request, status=None,pk=None):
        if(status == 'get'):
            doctor = get_object_or_404(Doctor, id = pk)
            sessions = doctor.sessions.is_ongoing()
            releted_doctor = Doctor.objects.filter(
                Q(hospital_name__icontains = doctor.hospital_name) |
                Q(chamber_address__icontains = doctor.chamber_address) |
                Q(qualification__icontains = doctor.qualification) |
                Q(specialty__icontains = doctor.specialty) 
            ).exclude(id=doctor.id).distinct()[:5]
            context = {
                'doctor':doctor,
                'sessions': sessions,
                'releted_doctor': releted_doctor
            }
            return render(request, 'doctor_profile.html', context )
        data = Doctor.objects.all()
        q = request.GET.get('q')
        if(q):
            print(q)
            data = data.filter(
                Q(hospital_name__icontains = q) |
                Q(user__first_name__icontains = q) |
                Q(user__last_name__icontains = q) |
                Q(chamber_address__icontains = q) |
                Q(qualification__icontains = q) |
                Q(specialty__icontains = q) 
            )
        paginator = Paginator(data, 12)
        page_number = request.GET.get('page')
        doctors = paginator.get_page(page_number)


        return render(request, 'doctor_list.html', {'doctors': doctors,'q':q})

