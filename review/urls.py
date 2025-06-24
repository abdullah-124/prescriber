from django.urls import path
from review.views import patient_review


urlpatterns = [
    path('patient/<int:id>/', patient_review, name = 'patient_review')
]
