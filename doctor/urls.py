from django.urls import path
from doctor import views
urlpatterns = [
    path('registration/', views.doctor_regestration, name='doctor_registration'),
    path('<str:status>/<int:pk>/', views.DoctorView.as_view(), name='doctor'),
    path('', views.DoctorView.as_view(), name='doctor_list'),
]
