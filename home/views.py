from django.shortcuts import render, redirect
from django.http import HttpResponse
#import datetime
#from datetime import date  # Import the date class
from .models import *
TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR,"templates")'
)

def index(request):
    return render(request, "home/index.html")

def login(request):
    if request.method == "POST":
        # Extract email and password from the request
        email = request.POST.get('email')
        password = request.POST.get('password')
        radio_option = request.POST.get('radio_options')
        print(radio_option)
        print("Email:", email)
        print("Password:", password)
        if(radio_option=="option1"):
            lst=login_student()
            flag=False
            for i in lst:
                if(i[0]==email and i[1]==password):
                    flag=True
                    break
            if(flag==True):
                # You can redirect or render a different template here if needed
                return redirect('/home')
            else:
                return HttpResponse("Failed!!")
        elif(radio_option=="option2"):
            lst=login_company()
            flag=False
            for i in lst:
                if(i[0]==email and i[1]==password):
                    flag=True
                    break
            if(flag==True):
                # You can redirect or render a different template here if needed
                return HttpResponse("Success!")# Example redirect to success page
            else:
                return HttpResponse("Failed!!")
        else:
            lst=login_admin()
            flag=False
            for i in lst:
                if(i[0]==email and i[1]==password):
                    flag=True
                    break
            if(flag==True):
                # You can redirect or render a different template here if needed
                return HttpResponse("Success!")# Example redirect to success page
            else:
                return HttpResponse("Failed!!")
    return render(request, 'home/login.html')


def student_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        date_of_birth = request.POST.get('dob')
        print(date_of_birth)
        gender = request.POST.get('gender')
        r_number = request.POST.get('r_number')
        department = request.POST.get('department')
        cgpa = request.POST.get('cgpa')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if email in student_regsiter_emails():
            return HttpResponse("Mail-id already registered")
        else:
            register_student(r_number,full_name,email,contact_number,date_of_birth,gender,department,cgpa,password)
            return render(request,"login.html")
    return render(request, 'home/student_register.html')


def company_register(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        street_number = request.POST.get('street_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        password = request.POST.get('password')
        if email in company_regsiter_emails():
            return HttpResponse("Mail-id already registered")
        else:
            register_company(company_name,email,contact_number,street_number,city,state,country,pincode,password)
            return render(request,"login.html")
    return render(request, 'home/company_register.html')


def password_reset(request):
    return render(request, 'home/password_reset.html')

def home(request):
    return render(request, 'home/jobboard.html')