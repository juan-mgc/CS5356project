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
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('radio_options')
        
        # Check if a User with this email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Login Failed: User does not exist")

        # Authenticate the user using the password
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            # Store user type in session to manage redirection
            if user_type == "option1" and hasattr(user, 'student'):
                request.session['user_type'] = 'student'
                return redirect('student_dashboard')
            elif user_type == "option2" and hasattr(user, 'company'):
                request.session['user_type'] = 'company'
                return redirect('company_dashboard')
            elif user_type == "option3" and hasattr(user, 'admin'):
                request.session['user_type'] = 'admin'
                return redirect('admin_dashboard')
            else:
                return HttpResponse("Login Failed: Incorrect user type")
        else:
            return HttpResponse("Login Failed: Incorrect credentials")
    
    return render(request, 'login.html')

def authenticate_user(model, email, password):
    try:
        user = model.objects.get(email=email, password=password)
        return True
    except model.DoesNotExist:
        return False


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

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def company_dashboard(request):
    return render(request, 'company_dashboard.html')

def password_reset(request):
    return render(request, '/password_reset.html')

def home(request):
    jobs = Job.objects.all()
    internships = Internship.objects.all()
    return render(request, 'jobboard.html', {'jobs': jobs, 'internships': internships})

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
            role=role,
            description=description,
            duration=duration,
            type=internship_type,
            location=location,
            stipend=stipend,
            company=company,
            created_by=admin
        )
        internship.save()
        
        return redirect("view_internships")  #redirect to list of internships after saving
    #GET request
    return render(request, "add_internship.html")
    
def add_job(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        company_id = request.POST.get("company_id")
        Job.objects.create(
            name=name,
            description=description,
            company_id=company_id,
            created_by=request.user
        )
        return redirect("view_jobs")
    return render(request, "add_job.html")
    
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
def view_student_profile(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
        if request.method == "POST":
            student.full_name = request.POST.get("full_name")
            student.contact_number = request.POST.get("contact_number")
            student.save()
            return redirect("view_student_profile")
        return render(request, 'view_student_profile.html', {'student': student})
    return HttpResponse("Unauthorized", status=401)

def view_internships(request):
    internships = Internship.objects.all()
    return render(request, 'view_internships.html', {'internships': internships})
def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    # note there should be a many-to-many field for applications
    internship.members_applied.add(request.user)
    return redirect("view_internships")

def view_jobs(request):
    jobs = Job.objects.all()
    return render(request, 'view_jobs.html', {'jobs': jobs})
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    # note there should be a many-to-many field for applications
    job.members_applied.add(request.user)
    return redirect("view_jobs")

@login_required
def view_notice(request):
    #retrieve the Student instance linked to the current user
    if hasattr(request.user, 'student'):
        student = request.user.student
        #filter notices for this student
        notices = Notice.objects.filter(recipient=student)
        return render(request, 'view_notice.html', {'notices': notices})
    else:
        return HttpResponse("Unauthorized", status=401)

def view_companies(request):
    companies = Company.objects.all()
    return render(request, 'view_companies.html', {'companies': companies})

def view_events(request):
    events = Event.objects.all()
    return render(request, 'view_events.html', {'events': events})

def logout_view(request):
    # Handle logout logic here (e.g., using Django's built-in logout function)
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'logout.html')  # Replace with your actual logout redirect template
