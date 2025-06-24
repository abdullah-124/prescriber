from django.urls import path
from precription import views

urlpatterns = [
    path('form/<int:id>/', views.make_prescription, name='prescription_form'),
    path('update_prescription/<int:id>/', views.PrescriptionUpdate_View.as_view(), name='prescription_update'),
    path('get/<int:id>/', views.Prescription_User_View.as_view(), name='get_prescription'),
    path('demo/',views.demo_prescription, name='demo_prescription')
]
