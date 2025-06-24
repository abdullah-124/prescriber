from django.urls import path
from appointment import views


urlpatterns = [
    path('',views.Appointment.as_view(), name='appointment_list'),
    path('action/<str:status>/', views.Appointment.as_view(), name='appointment'),
    path('action/<str:status>/<int:pk>/', views.Appointment.as_view(), name = 'appointment'),
    path('action/patient_list/<int:pk>/', views.Appointment.as_view(), name = 'patient_list'),
    path('search/',views.search_appointment, name='search_appointment'),
    path('add_patient/', views.Add_patient.as_view(), name="add_patient_doctor_view")
]
