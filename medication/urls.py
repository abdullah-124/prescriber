from django.urls import path
from .views import get_medicines_list


urlpatterns = [
    path('get_midicines/<int:id>/', get_medicines_list, name='get_medicines_list'),
]
