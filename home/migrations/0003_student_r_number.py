# Generated by Django 5.1.2 on 2024-10-24 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_admin_company_rename_age_student_cgpa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='r_number',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
