from django.urls import path
from user import views
urlpatterns = [
    path('register/',views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/', views.UserProfile.as_view(), name='user_profile'),
    path('profile/<str:status>/', views.UserProfile.as_view(), name='user_profile'),
]
