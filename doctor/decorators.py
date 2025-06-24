from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from functools import wraps
from doctor.models import Doctor

def doctor_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if (request.user.role == 'doctor'):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("You must be a doctor to access this page.")
    return _wrapped_view
class DoctorRequiredMixin(AccessMixin):
    # """Allow access only to users with role='doctor'."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_login')
        # print('hello form mixin')
        if getattr(request.user, 'role', None) != 'doctor':
            messages.error(request, "You have no permission to access this page.")
            return render(request, 'not_found.html')

        return super().dispatch(request, *args, **kwargs)