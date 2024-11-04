# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'), 
    path('student_register/', views.student_register, name='student_register'),
    path('company_register/', views.company_register, name='company_register'),
    path('home/', views.home, name='home'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),
    path('logout',views.index,name='logout'),
    #student profile
    path('view_student_profile/', views.view_student_profile, name='view_student_profile'),
    
    #internship related paths
    path('view_internships/', views.view_internships, name='view_internships'),
    path('apply_internship/<int:internship_id>/', views.apply_internship, name='apply_internship'),
    path('add_internship/', views.add_internship, name='add_internship'),
    
    #job related paths
    path('view_jobs/', views.view_jobs, name='view_jobs'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('add_job/', views.add_job, name='add_job'),
    
    #notice related paths
    path('view_notice/', views.view_notice, name='view_notice'),
    path('add_notice/', views.add_notice, name='add_notice'),
    
    #company related path
    path('view_companies/', views.view_companies, name='view_companies'),
    
    #event related paths
    path('view_events/', views.view_events, name='view_events'),
    path('add_event/', views.add_event, name='add_event'),
]