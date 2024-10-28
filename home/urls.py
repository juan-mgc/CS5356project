# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('student_register/', views.student_register, name='student_register'),
    path('company_register/', views.company_register, name='company_register'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('', views.home, name='home'),
]