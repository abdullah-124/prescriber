from django.urls import path
from drugs.views import search_drugs

urlpatterns = [
    path('search/', search_drugs, name='search_drugs'),
]
