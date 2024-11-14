from django.contrib.auth.models import User
from django.db import models
from datetime import * # Import the date class


# Create your models here.
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)  #custom primary Key
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    contact_number = models.BigIntegerField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100)
    r_number = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    cgpa = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)  #custom primary key
    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.IntegerField()
    street_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    def __str__(self):
        return str(self.company_id)

class Admin(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Internship(models.Model):
    internship_id = models.CharField(max_length=25, primary_key=True)
    internship_role = models.CharField(max_length=50)
    description = models.TextField()
    internship_type = models.CharField(
        max_length=20,
        choices=[
            ('part_time', 'Part Time'),
            ('full_time', 'Full Time'),
        ],
    )
    location = models.CharField(
        max_length=20,
        choices=[
            ('remote', 'Remote'),
            ('in_office', 'In Office'),
            ('hybrid', 'Hybrid'),
        ],
    )
    stipend = models.IntegerField()
    start_date = models.DateField()
    duration_months = models.IntegerField()
    last_date_to_apply = models.DateField()
    posted_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="internship")
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name="created_internships")

    def __str__(self):
        return f"{self.internship_role} at {self.company.company_name}"
    
class InternshipApplications(models.Model):
    internship_application_id = models.AutoField(primary_key=True)
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, related_name='internship_applications')  
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='internship_applications')
    date_of_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],default='Pending')

    def __str__(self):
        return f"{self.student.full_name} applied for {self.internship.Internship_name}"

class Job(models.Model):
    job_id = models.CharField(max_length=25, primary_key=True)
    job_role = models.CharField(max_length=50)  # Rename "name" to "job_role"
    description = models.TextField()
    job_type = models.CharField(
        max_length=20, choices=[('part_time', 'Part Time'), ('full_time', 'Full Time')]
    )
    location = models.CharField(
        max_length=20,
        choices=[('remote', 'Remote'), ('in_office', 'In Office'), ('hybrid', 'Hybrid')],
    )
    salary = models.IntegerField()
    start_date = models.DateField()
    last_date_to_apply = models.DateField()
    posted_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="job")
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name="created_jobs")

    def __str__(self):
        return f"{self.job_role} at {self.company.company_name}"
    
class JobApplications(models.Model):
    job_application_id = models.AutoField(primary_key=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='job_applications')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='job_applications')
    date_of_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.student.name} applied for {self.job.job_name}"

#notices in student_board
class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    announcement_text = models.TextField()
    created_by = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True)
    recipient_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)

#Login
def login_student():
    students = Student.objects.all()
    lst=[]
    for student in students:
    	lst.append([student.email,student.password])
    return lst

def login_company():
    companies = Company.objects.all()
    lst=[]
    for company in companies:
    	lst.append([company.email,company.password])
    return lst

def login_admin():
    admins = Admin.objects.all()
    lst=[]
    for admin in admins:
    	lst.append([admin.email,admin.password])
    return lst

def student_regsiter_emails():
    students = Student.objects.all()
    lst=[]
    for student in students:
        lst.append(student.email)
    return lst

def company_regsiter_emails():
    companies = Company.objects.all()
    lst=[]
    for company in companies:
        lst.append(company.email)
    return lst


#Register
def register_student(r_number,full_name,email,contact_number,date_of_birth,gender,department,cgpa,password):
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

def register_company(company_name,email,contact_number,street_number,city,state,country,pincode,password):
    company_count = Company.objects.count()
    new_company=Company(
        company_id=company_count+1,
        company_name=company_name,
        email=email,
        contact_number=contact_number,
        street_number=street_number,
        city=city,
        state=state,
        country=country,
        pincode=pincode,
        password=password
        )
    new_company.save()

'''
new_student = Student(
    student_id='1',
    full_name='Sruthi Mandalapu',
    city='Lubbock',
    state='Texas',
    pincode='79415',
    email='sruthimandalapu@gmail.com', 
    contact_number='8067026486',          
    age=23,
    gender='female',
    date_of_birth=date(1925, 4, 10),
    password='sruthi'
)

from django.contrib.auth.models import User
from home.models import Student

#create a User instance
user = User.objects.create_user(username='sruthimandalapu@gmail.com', email='sruthimandalapu@gmail.com', password='sruthi')

#retrieve the existing Student and link the User
student = Student.objects.get(email='sruthimandalapu@gmail.com')
student.user = user
student.save()

'''
