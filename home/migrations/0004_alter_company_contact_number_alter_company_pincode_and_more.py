# Generated by Django 5.1.2 on 2024-10-25 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_student_r_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='contact_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='pincode',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='contact_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
