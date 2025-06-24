from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from user.models import User
from patient.models import Patient
from user.forms import UserRegestrationForm, UserUpdateForm
# Create your views here.


# USER CREATION
def user_register(request):
    if(request.user.is_authenticated):
        return render(request, 'not_found.html')
    if(request.method=='POST'):
        form = UserRegestrationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            login(request, user)
            return redirect('home')
    else :
        form = UserRegestrationForm()
    return render(request, 'register.html', {'form':form})

# USER LOGOUT

class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'home'
# ################

# USER LOGIN
def user_login(request):
    # print('hello login')
    if(request.user.is_authenticated):
        return render(request, 'not_found.html')
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        # # print(next_url)
        # user = authenticate(username = username, password = password)
        print(username,password)
        # if(user):
        #     # print('under the sea')
        #     login(request, user=user)
        #     return redirect(next_url) if next_url else redirect('home')
        # else:
        #     messages.error(request, 'invalid information ')
        try:
            user = User.objects.get(username=username)
            print(user)
            if not user.check_password(password):
                messages.error(request, "Incorrect password.")
            else :
                login(request, user)
                return redirect(next_url) if next_url else redirect('user_profile')
        except User.DoesNotExist:
            messages.error(request, "User does't exist.")

    return render(request, 'login.html')

class UserProfile(LoginRequiredMixin, View):
    def get(self,request,status = None):
        if(status=='update'):
            form = UserUpdateForm(instance=request.user)
            return render(request, 'update_user_profile.html', {'form':form})
        elif(status == 'password_change'):
            form = PasswordChangeForm(request.user)
            return render(request, 'password_change.html', {'form':form})
        user = get_object_or_404(User, username=request.user.username)
        patients = user.my_patients.all()
        context = {
            'user': user,
            'patients': patients
        }
        return render(request, 'user_profile.html', context)
    def post(self,request, status=None):
        # update profile info
        if(status=='update'):
            form = UserUpdateForm(request.POST,request.FILES, instance=request.user)
            if(form.is_valid()):
                photo = request.POST.get('photo')
                print(photo)
                messages.success(request, "Profile Updated")
                form.save()
                return redirect('user_profile')
            return render(request, 'update_user_profile.html', {'form':form})
        # password change formn
        elif status == 'password_change':
            form = PasswordChangeForm(user=request.user, data = request.POST)
            if(form.is_valid()):
                form.save()
                logout(request)
                messages.success(request, "Your password has changed. </br> please login with new password")
                return redirect('user_login')
            else:
                messages.error(request, form.errors)
            return render(request, 'password_change.html', {'form':form})
        return HttpResponse('<h1>Method not allowed</h1>')