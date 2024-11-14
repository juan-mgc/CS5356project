from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR,"templates")'
)

def index(request):
    return render(request, "index.html")

# def login_view(request):
#     if request.method == "POST":
#         # Extract email and password from the request
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         radio_option = request.POST.get('radio_options')
#         print(radio_option)
#         print("Email:", email)
#         print("Password:", password)
#         if(radio_option=="option1"):
#             lst=login_student()
#             flag=False
#             for i in lst:
#                 if(i[0]==email and i[1]==password):
#                     flag=True
#                     break
#             if(flag==True):
#                 request.session['user_type'] = 'student'
#                 return redirect('student_dashboard')
#             else:
#                 return HttpResponse("Failed!!")
#         elif(radio_option=="option2"):
#             lst=login_company()
#             flag=False
#             for i in lst:
#                 if(i[0]==email and i[1]==password):
#                     flag=True
#                     break
#             if(flag==True):
#                 request.session['user_type'] = 'company'
#                 return redirect('company_dashboard')
#             else:
#                 return HttpResponse("Failed!!")
#         else:
#             lst=login_admin()
#             flag=False
#             for i in lst:
#                 if(i[0]==email and i[1]==password):
#                     flag=True
#                     break
#             if(flag==True):
#                 request.session['user_type'] = 'admin'
#                 return redirect('admin_dashboard')
#             else:
#                 return HttpResponse("Failed!!")
#     return render(request, "login.html")
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        radio_option = request.POST.get('radio_options')
        user_authenticated = False

        if radio_option == "option1":  # student
            student = Student.objects.filter(email=email, password=password).first()
            if student:
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.set_password(password)
                    user.save()
                login(request, user)
                request.session['user_type'] = 'student'
                request.session['user_email'] = email
                user_authenticated = True

        elif radio_option == "option2":  # company
            company = Company.objects.filter(email=email, password=password).first()
            if company:
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.set_password(password)
                    user.save()
                login(request, user)
                request.session['user_type'] = 'company'
                request.session['user_email'] = email
                user_authenticated = True

        else:  # admin
            admin = Admin.objects.filter(email=email, password=password).first()
            if admin:
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.set_password(password)
                    user.save()
                login(request, user)
                request.session['user_type'] = 'admin'
                request.session['user_email'] = email
                user_authenticated = True

        #redirect based on user type
        if user_authenticated:
            if request.session['user_type'] == 'student':
                return redirect('student_dashboard')
            elif request.session['user_type'] == 'company':
                return redirect('company_dashboard')
            else:
                return redirect('admin_dashboard')
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, "login.html")

def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        #confirm_password = request.POST.get('confirm_password')
        radio_option = request.POST.get('radio_options')
        if radio_option=="option1":
            lst=student_regsiter_emails()
            if email in lst:
                update_student_password(email,password)
            else:
                return HttpResponse("Email is not registered")
        elif radio_option=="option2":
            lst=company_regsiter_emails()
            if email in lst:
                update_company_password(email,password)
            else:
                return HttpResponse("Email is not registered")
        else:
            lst=admin_regsiter_emails()
            if email in lst:
                update_admin_password(email,password)
            else:
                return HttpResponse("Email is not registered")
    return render(request, 'password_reset.html')

def home(request):
    jobs = Job.objects.all()
    internships = Internship.objects.all()
    return render(request, 'jobboard.html', {'jobs': jobs, 'internships': internships})

#def logout_view(request):
    # Handle logout logic here (e.g., using Django's built-in logout function)
    #from django.contrib.auth import logout
    #logout(request)
    #return render(request, 'logout.html')  # Replace with your actual logout redirect template
    

# ADMIN
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

#fetch a particular admin by ID
def fetch_admin_details(admin_id):
    admin=Admin.objects.get(admin_id=admin_id)
    lst = [
        admin.full_name,
        admin.email,
        admin.contact_number,
        admin.age,
        admin.gender,
    ]
    return lst

#update deatils of a particular admin by ID
def update_admin_details(admin_id,full_name,email,contact_number,age,gender):
    admin=Admin.objects.get(admin_id=admin_id)
    admin.full_name=full_name
    admin.email=email
    admin.contact_number=contact_number
    admin.age=age
    admin.gender=gender
    company.save()

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

#creates a new student record in the DB
def create_student_record(full_name,email,contact_number,date_of_birth,gender,r_number,department,cgpa,password):
    student_count = Student.objects.count()
    new_student=Student(
        student_id=student_count+1,
        full_name=full_name,
        email=email,
        contact_number=contact_number,
        date_of_birth=date_of_birth,
        gender=gender,
        r_number=r_number,
        department=department,
        cgpa=cgpa,
        password=password
        )
    new_student.save()

def update_student_password(email,password):
    student=Student.objects.get(email=email)
    student.password=password
    student.save()

def update_admin_password(email,password):
    admin=Admin.objects.get(email=email)
    admin.password=password
    admin.save()
    
#updates details of a particular student by ID
def update_student_record(student_id,full_name,email,contact_number,date_of_birth,gender,r_number,department,cgpa):
    student=Student.objects.get(student_id=student_id)
    student.full_name=full_name
    student.email=email
    student.contact_number=contact_number
    student.date_of_birth=date_of_birth
    student.gender=gender
    student.r_number=r_number
    student.department=department
    student.cgpa=cgpa
    #student.password=password
    student.save()
    
def view_particular_student(student_id):
    student=Student.objects.get(student_id=student_id)
    lst=[]
    lst.append(student.full_name)
    lst.append(student.email)
    lst.append(student.contact_number)
    lst.append(student.date_of_birth)
    lst.append(student.gender)
    lst.append(student.r_number)
    lst.append(student.department)
    lst.append(student.cgpa)
    return lst

#fetch details of all studnets as a list of lists
def fetch_all_students():
    students = Student.objects.all()
    result = [
        [
            student.student_id,
            student.full_name,
            student.email,
            student.contact_number,
            student.date_of_birth,
            student.gender,
            student.r_number,
            student.department,
            student.cgpa,
        ]
        for student in students
    ]
    return result
    
def delete_student(student_id):
    student=Student.objects.get(student_id=student_id)
    student.delete()

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def view_student_profile(request):
    print(f"Session Data: {request.session.items()}")  # Debug session data
    print(f"User Authenticated: {request.user.is_authenticated}")  # Check user authentication

    if request.session.get('user_type') == 'student':
        student = get_object_or_404(Student, email=request.session.get('user_email'))
        return render(request, 'view_student_profile.html', {'student': student})
    return HttpResponse("Unauthorized access", status=401)

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

#creates a new company record in DB
def create_company_record(company_name,email,contact_number,street_number,city,state,country,pincode):
    company_count = Company.objects.count()
    new_company = Company(
        company_id=company_count + 1,
        company_name=company_name,
        email=email,
        contact_number=contact_number,
        street_number=street_number,
        city=city,
        state=state,
        country=country,
        pincode=pincode,
    )
    new_company.save()

def update_company_password(email,password):
    company=Company.objects.get(email=email)
    company.password=password
    company.save()
    
#update details of a particular company by ID
def update_company_record(company_id,company_name,email,contact_number,street_number,city,state,country,pincode):
    company = Company.objects.get(company_id=company_id)
    company.company_name = company_name
    company.email = email
    company.contact_number = contact_number
    company.street_number = street_number
    company.city = city
    company.state = state
    company.country = country
    company.pincode = pincode
    company.save()
    
def delete_company(company_id):
    company=Company.objects.get(company_id=company_id)
    company.delete()
    
def view_particular_company(company_id):
    company=Company.objects.get(company_id=company_id)
    lst=[]
    lst.append(company.company_name)
    lst.append(company.email)
    lst.append(company.contact_number)
    lst.append(company.street_number)
    lst.append(company.city)
    lst.append(company.state)
    lst.append(company.country)
    lst.append(company.pincode)
    return lst

#fetches all company details as a list of lists
def fetch_all_companies():
    companies = Company.objects.all()
    e=[]
    for company in companies:
        lst=[]
        lst.append(company.company_id)
        lst.append(company.company_name)
        lst.append(company.email)
        lst.append(company.contact_number)
        lst.append(company.street_number)
        lst.append(company.city)
        lst.append(company.state)
        lst.append(company.country)
        lst.append(company.pincode)
        e.append(lst)
    return e

def company_dashboard(request):
    return render(request, 'company_dashboard.html')

@login_required
def company_profile(request):
    if hasattr(request.user, 'company'):  #check if the logged-in user has a company profile
        company = request.user.company
        if request.method == "POST":
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

#creates a new internship record in DB
def create_internship_record(internship_id,role,description,duration,type,location,stiphend,company,created_by,posted_date):
    internship_count = Internship.objects.count()
    new_internship=Internship(
        internship_id=internship_count+1,
        role=role,
        description=description,
        duration=duration,
        type=type,
        location=location,
        stiphend=stiphend,
        company=company,
        created_by=created_by,
        posted_date=posted_date
        )
    new_internship.save()

#updates internship details in the database by ID
def update_internship_record(internship_id,role,description,duration,type,location,stiphend,company,created_by,posted_date):
    internship=Internship.objects.get(internship_id=internship_id)
    internship.role=role
    internship.description=description
    internship.duration=duration
    internship.type=type
    internship.location=location
    internship.stiphend=stiphend
    internship.company=company
    internship.created_by=created_by
    internship.posted_date=posted_date
    internship.save()

def view_internships(request):
    internships = Internship.objects.all()
    return render(request, 'view_internships.html', {'internships': internships})

def delete_internship(internship_id):
    internship=Internship.objects.get(internship_id=internship_id)
    internship.delete()
    
def view_particular_internship(internship_id):
    internship=Internship.objects.get(internship_id=internship_id)
    lst=[]
    lst.append(internship.role)
    lst.append(internship.description)
    lst.append(internship.duration)
    lst.append(internship.type)
    lst.append(internship.location)
    lst.append(internship.stiphend)
    lst.append(internship.company)
    lst.append(internship.created_by)
    lst.append(internship.posted_date)
    return lst

#fetches all internship details as a list of lists
def fetch_all_internships():
    internships = Internship.objects.all()
    e=[]
    for internship in internships:
        lst=[]
        lst.append(internship.intership_id)
        lst.append(internship.role)
        lst.append(internship.description)
        lst.append(internship.duration)
        lst.append(internship.type)
        lst.append(internship.location)
        lst.append(internship.stiphend)
        lst.append(internship.company)
        lst.append(internship.created_by)
        lst.append(internship.posted_date)
        e.append(lst)
    return e

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

#creates a new job record in DB
def create_job_record(job_id,name,description,company,created_by,posted_date):
    job_count = Job.objects.count()
    new_job=Job(
        job_id=internship_count+1,
        name=name,
        description=description,
        company=company,
        created_by=created_by,
        posted_date=posted_date
        )
    new_job.save()
    
#updates job details in the database by ID
def update_job_record(job_id,name,description,company,created_by,posted_date):
    job=Job.objects.get(job_id=job_id)
    job.name=name
    job.description=description
    job.company=company
    job.created_by=created_by
    job.posted_date=posted_date
    job.save()
    
def delete_job(job_id):
    job=Job.objects.get(job_id=job_id)
    job.delete()
    
def view_particular_job(job_id):
    job=Job.objects.get(job_id=job_id)
    lst=[]
    lst.append(job.name)
    lst.append(job.description)
    lst.append(job.company)
    lst.append(job.created_by)
    lst.append(job.posted_date)
    return lst

#fetches all job details as a list of lists
def fetch_all_jobs():
    jobs = Jobs.objects.all()
    e=[]
    for job in jobs:
        lst=[]
        lst.append(job.name)
        lst.append(job.description)
        lst.append(job.company)
        lst.append(job.created_by)
        lst.append(job.posted_date)
        e.append(lst)
    return e

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

#creates a new event record in DB
def create_event_record(event_id,title,description,date,location):
    event_count = Event.objects.count()
    new_event=Event(
        event_id=event_count+1,
        title=title,
        description=description,
        date=date,
        location=location
        )
    new_event.save()
    
#updates event details in the database by ID
def update_event_record(event_id,title,description,date,location):
    event=Event.objects.get(event_id=event_id)
    event.title=title
    event.description=description
    event.date=date
    event.location=location
    event.save()
    
def view_events(request):
    events = Event.objects.all()
    user_type = request.session.get('user_type', None)
    can_manage_events = user_type in ['admin', 'company']
    return render(request, 'view_events.html', {'events': events, 'can_manage_events': can_manage_events})

#fetches all event details as a list of lists
def fetch_all_events():
    events = Event.objects.all()
    e=[]
    for event in events:
        lst=[]
        lst.append(event.event_id)
        lst.append(event.title)
        lst.append(event.description)
        lst.append(event.date)
        lst.append(event.location)
        e.append(lst)
    return e

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

#creates a new notice record in DB
def create_notice_record(notice_id,announcement_text,created_by,recipient,date_created):
    notice_count = Notice.objects.count()
    new_notice=Notice(
        notice_id=notice_count+1,
        announcement_text=announcement_text,
        created_by=created_by,
        recipient=recipient,
        date_created=date_created
        )
    new_notice.save()

@login_required
def view_notice(request):
    user_type = request.session.get('user_type')
    if user_type == 'student':
        student = get_object_or_404(Student, email=request.session.get('user_email'))
        notices = Notice.objects.filter(recipient_id=student.student_id)
    elif user_type == 'admin':
        admin = get_object_or_404(Admin, email=request.session.get('user_email'))
        notices = Notice.objects.filter(created_by=admin)
    elif user_type == 'company':
        notices = Notice.objects.all()
    else:
        return HttpResponse("Unauthorized access", status=401)
    return render(request, 'view_notice.html', {'notices': notices})

#fetches all notice details as a list of lists
def fetch_all_notices():
    notices = Notice.objects.all()
    e=[]
    for notice in notices:
        lst=[]
        lst.append(notice.announcement_text)
        lst.append(notice.created_by)
        lst.append(notice.recipient)
        lst.append(notice.created_by)
        e.append(lst)
    return e

#updates notice details in the database by ID
def update_notice_record(notice_id,announcement_text,created_by,recipient,date_created):
    notice=Notice.objects.get(notice_id=notice_id)
    notice.announcement_text=announcement_text
    notice.created_by=created_by
    notice.recipient=recipient
    notice.date_created=date_created
    notice.save()
    
def delete_notice(notice_id):
    notice=Notice.objects.get(notice_id=notice_id)
    notice.delete()
    
def view_particular_notice(notice_id):
    notice=Notice.objects.get(notice_id=notice_id)
    lst=[]
    lst.append(notice.announcement_text)
    lst.append(notice.created_by)
    lst.append(notice.recipient)
    lst.append(notice.created_by)
    return lst