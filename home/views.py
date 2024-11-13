from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR,"templates")'
)

def index(request):
    return render(request, "index.html")

def login_view(request):
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
                request.session['user_type'] = 'student'
                return redirect('student_dashboard')
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
                request.session['user_type'] = 'company'
                return redirect('company_dashboard')
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
                request.session['user_type'] = 'admin'
                return redirect('admin_dashboard')
            else:
                return HttpResponse("Failed!!")
    return render(request, "login.html")

def password_reset(request):
    return render(request, '/password_reset.html')

def home(request):
    jobs = Job.objects.all()
    internships = Internship.objects.all()
    return render(request, 'jobboard.html', {'jobs': jobs, 'internships': internships})

def logout_view(request):
    # Handle logout logic here (e.g., using Django's built-in logout function)
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'logout.html')  # Replace with your actual logout redirect template

# ADMIN
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# STUDENT
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
    return render(request, 'student_register.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def view_student_profile(request):
    if request.session.get('user_type') == 'student':
        student = get_object_or_404(Student, email=request.user.email)
        return render(request, 'view_student_profile.html', {'student': student})
    return HttpResponse("Unauthorized", status=401)

def view_students(request):
    # Check if the user is an admin
    if request.session.get('user_type') == 'admin':
        students = Student.objects.all()
        return render(request, 'view_students.html', {'students': students})
    return HttpResponse("Unauthorized", status=401)

# COMPANY
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
    return render(request, 'company_register.html')

def company_dashboard(request):
    return render(request, 'company_dashboard.html')

def view_companies(request):
    companies = Company.objects.all()
    return render(request, 'view_companies.html', {'companies': companies})

@login_required
def company_profile(request):
    if hasattr(request.user, 'company'):  # Check if the logged-in user has a company profile
        company = request.user.company  # Access the linked company profile
        if request.method == "POST":
            # Update company details if submitted
            company.company_name = request.POST.get("company_name", company.company_name)
            company.contact_number = request.POST.get("contact_number", company.contact_number)
            company.street_number = request.POST.get("street_number", company.street_number)
            company.city = request.POST.get("city", company.city)
            company.state = request.POST.get("state", company.state)
            company.country = request.POST.get("country", company.country)
            company.pincode = request.POST.get("pincode", company.pincode)
            company.save()
            return redirect("company_profile")
        return render(request, 'company_profile.html', {'company': company})
    return HttpResponse("Unauthorized", status=401)

#INTERNSHIP
def add_internship(request):
    if request.method == "POST":
        #fetch form data
        role = request.POST.get("role")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        internship_type = request.POST.get("type")
        location = request.POST.get("location")
        stipend = request.POST.get("stipend")
        
        company = Company.objects.first()  #replace with dynamic data if needed
        admin = Admin.objects.first()  #replace with the actual admin creating the post

        #create and save the Internship instance
        internship = Internship(
            internship_role = role,
            description = description,
            internship_type = internship_type,
            location = location,
            stipend = stipend,
            start_date = start_date,
            duration = duration,
            company = company,
            last_date_to_apply = last_date_to_apply,
            posted_date = posted_date,
        )
        internship.save()
        
        return redirect("view_internships")  #redirect to list of internships after saving
    #GET request
    return render(request, "add_internship.html")

def view_internships(request):
    internships = Internship.objects.all()
    return render(request, 'view_internships.html', {'internships': internships})

def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    # note there should be a many-to-many field for applications
    internship.members_applied.add(request.user)
    return redirect("view_internships")

# JOB
def add_job(request):
    if request.method == "POST":
        job_id=request.POST.get("job_id")
        role = request.POST.get("role")
        description = request.POST.get("description")
        job_type = request.POST.get("type")
        location = request.POST.get("location")
        salary = request.POST.get("salary")
        start_date = request.POST.get("start_date")
        last_date_to_apply = request.POST.get("last_date_to_apply")
        posted_date = date.today()
        company = Company.objects.first()

        #create and save the Internship instance
        job = Job(
            job_id = job_id,
            job_role = role,
            description = description,
            job_type = job_type,
            location = location,
            salary = salary,
            start_date = start_date,
            company = company,
            last_date_to_apply = last_date_to_apply,
            posted_date = posted_date,
        )
        job.save()
        
        return redirect("view_jobs")
    return render(request, "add_job.html")

def view_jobs(request):
    jobs = Job.objects.all()
    return render(request, 'view_jobs.html', {'jobs': jobs})

def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    # note there should be a many-to-many field for applications
    job.members_applied.add(request.user)
    return redirect("view_jobs")

# EVENT
def add_event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        location = request.POST.get("location")
        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location
        )
        return redirect("view_events")
    return render(request, "add_event.html")

@login_required
def view_events(request):
    events = Event.objects.all()
    user_type = request.session.get('user_type', None)
    can_manage_events = user_type in ['admin', 'company']
    return render(request, 'view_events.html', {'events': events, 'can_manage_events': can_manage_events})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.session.get('user_type') not in ['admin', 'company']:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        event.title = request.POST.get("title", event.title)
        event.description = request.POST.get("description", event.description)
        event.date = request.POST.get("date", event.date)
        event.location = request.POST.get("location", event.location)
        event.save()
        return redirect('view_events')
    return render(request, 'edit_event.html', {'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.session.get('user_type') not in ['admin', 'company']:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        event.delete()
        return redirect('view_events')
    return render(request, 'delete_event.html', {'event': event})

@login_required
def dashboard(request):
    user_type = request.session.get('user_type')
    if user_type == 'student':
        return redirect('student_dashboard')
    elif user_type == 'company':
        return redirect('company_dashboard')
    elif user_type == 'admin':
        return redirect('admin_dashboard')
    return HttpResponse("Unauthorized", status=401)

# NOTICE
def add_notice(request):
    if request.method == "POST":
        announcement_text = request.POST.get("announcement_text")
        recipient_id = request.POST.get("recipient_id")
        Notice.objects.create(
            announcement_text=announcement_text,
            recipient_id=recipient_id,
            created_by=request.user
        )
        return redirect("view_notice")
    return render(request, "add_notice.html")

@login_required
def view_notice(request):
    if request.session.get('user_type') == 'student':
        student = get_object_or_404(Student, email=request.user.email)
        notices = Notice.objects.filter(recipient=student)
        return render(request, 'view_notice.html', {'notices': notices})
    return HttpResponse("Unauthorized", status=401)