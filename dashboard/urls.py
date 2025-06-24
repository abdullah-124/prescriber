from django.urls import path
from dashboard import views
from appointment.views import Session
from doctor.views import Doctor_profile 

urlpatterns = [
    path('', views.overview, name='dashboard_overview'),
    path('appointment/', Session.as_view(), name='dashboard_appointment_list'),
    path('appointment/<str:action>/', Session.as_view(), name='dashboard_appointment'),
    path('appointment/<str:action>/<int:pk>/', Session.as_view(), name='appointment_operation'),
    path('appointment/get/<int:pk>/', Session.as_view(), name='get_patient_list'),
    path('profile/', Doctor_profile.as_view(), name='doctor_profile'),
    path('profile/<str:status>/', Doctor_profile.as_view(), name='doctor_profile')
]
