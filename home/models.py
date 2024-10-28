from django.db import models
from datetime import * # Import the date class


# Create your models here.
class Student(models.Model):
    student_id=models.IntegerField()
    full_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contact_number=models.IntegerField()
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=100)
    r_number=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    cgpa=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return str(self.student_id)

class Company(models.Model):
    company_id=models.IntegerField()
    company_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contact_number=models.IntegerField()
    street_number=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    pincode=models.IntegerField()
    password=models.CharField(max_length=100)
    def __str__(self):
        return str(self.student_id)

class Admin(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contact_number=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return str(self.student_id)



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

# Save the instance to the database
new_student.save()

# from home.models import Student
#Student.objects.all()



 from home.models import Student
 students = Student.objects.all()

'''
