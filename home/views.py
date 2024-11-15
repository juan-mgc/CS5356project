from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *
from datetime import date
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
        intersnship_id=request.POST.get("internship_id")
        role = request.POST.get("role")
        description = request.POST.get("description")
        internship_type = request.POST.get("type")
        location = request.POST.get("location")
        stipend = request.POST.get("stipend")
        start_date = request.POST.get("start_date")
        duration = request.POST.get("duration")
        last_date_to_apply = request.POST.get("last_date_to_apply")
        posted_date = date.today()
        company = Company.objects.first()


        #create and save the Internship instance
        internship = Internship(
            intersnship_id = intersnship_id,
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
        
        return redirect("view_jobs")  #redirect to list of internships after saving
    #GET request
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

# company profile 

def company_profile(request, company_id):
    # Fetch the company details using company_id
    company = get_object_or_404(Company, company_id=company_id)
    return render(request, 'company_profile.html', {'company': company})

  
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
    student = request.user 
    # Create a new InternshipApplications entry
    InternshipApplications.objects.create(
        internship=internship,
        student=student,
        status='Pending'
    )
    return redirect("view_internships")


def view_jobs(request):
    jobs = Job.objects.all()
    return render(request, 'view_jobs.html', {'jobs': jobs})


def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    student = request.user
    # Create a new JobApplications entry
    JobApplications.objects.create(
        job=job,
        student=student,
        status='Pending'
    )
    return redirect("view_jobs")


# viewing job and intership applications

@login_required
def view_job_applications(request):
    if not hasattr(request.user, 'company'):
        return HttpResponse("Unauthorized", status=401)

    company = request.user.company
    jobs = Job.objects.filter(company=company)
    job_applications = JobApplications.objects.filter(job__in=jobs).select_related('student')
    return render(request, "view_job_applications.html", {"job_applications": job_applications})

@login_required
def view_internship_applications(request):
    if not hasattr(request.user, 'company'):
        return HttpResponse("Unauthorized", status=401)

    company = request.user.company
    internships = Internship.objects.filter(company=company)
    internship_applications = InternshipApplications.objects.filter(internship__in=internships).select_related('student')
    return render(request, "view_internship_applications.html", {"internship_applications": internship_applications})



# updating the hob and intership application status

@require_POST
@login_required
def update_job_application_status(request, application_id):
    if not hasattr(request.user, 'company'):
        return HttpResponse("Unauthorized", status=401)

    application = get_object_or_404(JobApplications, pk=application_id)
    if application.job.company != request.user.company:
        return HttpResponse("Unauthorized", status=401)

    new_status = request.POST.get("status")
    if new_status in ["Pending", "Accepted", "Rejected"]:
        application.status = new_status
        application.save()
    return redirect('view_job_applications')


@require_POST
@login_required
def update_internship_application_status(request, application_id):
    if not hasattr(request.user, 'company'):
        return HttpResponse("Unauthorized", status=401)

    application = get_object_or_404(InternshipApplications, pk=application_id)
    if application.internship.company != request.user.company:
        return HttpResponse("Unauthorized", status=401)

    new_status = request.POST.get("status")
    if new_status in ["Pending", "Accepted", "Rejected"]:
        application.status = new_status
        application.save()
    return redirect('view_internship_applications')





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
