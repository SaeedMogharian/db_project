from django.db import models
from core.models import UserAccount
from student.models import Student
from advisor.models import Advisor, Professor

# Create your models here.
class EducationalStat(models.Model):
    start_date = models.DateField()
    graduation_date = models.DateField()
    major = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=5, decimal_places=2)
    institution_name = models.CharField(max_length=255)
class Department(models.Model):
    name = models.CharField(max_length=255)

class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class Class(models.Model):
    class Schedule(models.Model):
        DAY_CHOICES = [
            ("Sat", "Saturday"),
            ("Sun", "Sunday"),
            ("Mon", "Monday"),
            ("Tue", "Tuesday"),
            ("Wed", "Wednesday"),
            ("Thu", "Thursday"),
            ("Fri", "Friday"),
        ]
        weekday = models.Choices(choices=DAY_CHOICES, max_length=10)
        start_time = models.TimeField()
        end_time = models.TimeField()
    course = models.ForeignKey(Course, null= False, on_delete=models.CASCADE)
    intructor = models.ForeignKey(Professor, null= False, on_delete=models.CASCADE)
    schedule = models.ManyToManyField(Schedule, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class AdvisingNote(models.Model):
    content = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed

# class AdvisingAppointment(models.Model):
#     date = models.DateField()
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
#     # Add other fields as needed

class Enrollment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    class_course = models.ForeignKey(Class, on_delete=models.CASCADE)
    # Add other fields as needed

class CoursePrecondition(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    precondition = models.ManyToManyField(Course, on_delete=models.CASCADE)
    # Add other fields as needed

    # check if unique
    # check if not precondition itself

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()