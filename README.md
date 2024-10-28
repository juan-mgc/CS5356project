#CS5356 project

## Requirements
To install the required dependencies, use the following command:

```bash
pip install django
```

## How to Run the Program
1. Open a terminal in the project folder.
2. Start the Django development server with:

   ```bash
   python manage.py runserver
   ```

## Checking the Inbuilt Django Database
To interact with the database, you can use Django's shell. Follow these steps:

1. Run migrations (if not already done):

   ```bash
   python manage.py migrate
   ```

2. Open the Django shell:

   ```bash
   python manage.py shell
   ```

3. Sample command: retrieve all student entries:

   ```python
   from home.models import Student
   Student.objects.all().values()
   ```

4. Exit the shell:

   ```bash
   exit()
   ```

## Available Pages
- **Login Page**: `/home/login`
- **Home Page**: `/home/index`
- **Student Registration**: `/home/student_register`
- **Company Registration**: `/home/company_register`
- **Password Reset**: `/home/password_reset`

---
