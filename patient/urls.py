from django.urls import path
from patient import views

urlpatterns = [
    path('profile/<int:id>/', views.patient_profile, name='patient_profile_doctor_view'),
    path('<int:id>/', views.Patient_profile_User_view.as_view(), name='patient_profile_user_view'),
    path('my_patients/', views.MyPatient.as_view(), name='my_patients'),
    path('delete/<int:pk>/', views.Patient_delete.as_view(), name='delete_patient')
]
