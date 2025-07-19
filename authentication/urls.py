from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
]