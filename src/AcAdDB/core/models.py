import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PhoneNumber(models.Model):
    PHONE_TYPES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"))
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=6, choices=PHONE_TYPES, default="Mobile")


class Major(models.Model):
    name = models.CharField(max_length=255)
    requierd_credit = models.IntegerField(max_length=10)
    cataloge = models.FileField(upload_to="/static/majors")


class EducationalStat(models.Model):
    start_date = models.DateField()
    graduation_date = models.DateField()
    major = models.ForeignKey(Major, on_delete=models.SET_NULL)
    degree = models.CharField(max_length=255)
    avg_grade = models.DecimalField(max_digits=5, decimal_places=2)
    institution_name = models.CharField(max_length=255)


class UserAccount(models.Model):
    class Meta:
        verbose_name = "User"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    GENDER_TYPES = (("M", "Male"), ("F", "Female"))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=255)
    national_code = models.CharField(max_length=20, unique=True)
    educational_stat = models.ManyToManyField(EducationalStat, blank=True)
    phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)
    email_address = models.EmailField(max_length=254)
    address = models.CharField(max_length=1000)

    def get_age(self):
        """
        Calculate and return user age.
        """
        current_year = datetime.datetime.now()
        birth_year = self.date_of_birth
        return (current_year - birth_year).year

    def get_first_name(self):
        """
        Return the first_name.
        """
        return self.first_name

    def get_last_name(self):
        """
        Return the last_name.
        """
        return self.last_name

    def get_full_name(self):
        """
        Return the first_name and last_name.
        """
        return f"{self.first_name} {self.last_name}"


class Department(models.Model):
    name = models.CharField(max_length=255)


class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, blank=True, on_delete=models.SET_DEFAULT)
    cred = models.IntegerField(default=1, max=10)
    description = models.TextField()

class CoursePrerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    prerequisites = models.ManyToManyField(Course, related_name="pre_req")

    # check if unique
    # check if not precondition itself


class Professor(UserAccount):
    class Meta:
        verbose_name = "professor"

    RANK_CHOICES = [
        ("Instructor", "Instructor"),
        ("Assistant Professor", "Assistant Professor"),
        ("Associative Professor", "Associative Professor"),
        ("Full Professor", "Full Professor"),
    ]
    rank = models.CharField(max_length=255, choices=RANK_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Advisor(Professor):
    advisor_id = models.CharField(max_length=15, unique=True)


class Term(models.Model):
    numerical_id = models.IntegerField(max_length=4, unique=True, primary_key=True)


class Event(models.Model):
    name = models.CharField(max_length=25)
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)


class TermEvent(Event):
    TYPE_CHOICES = [
        ("preregister", "preregister"),
        ("term", "Term"),
        ("class", "Class"),
        ("register", "Register"),
        ("adjustment", "Adjustment"),
        ("drop", "Drop"),
        ("exams", "Exams"),
    ]
    name = models.CharField(choices=TYPE_CHOICES, max_length=25)
    term = models.ForeignKey(Term, related_name="events", on_delete=models.CASCADE)


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
        weekday = models.CharField(choices=DAY_CHOICES, max_length=10)
        start_time = models.TimeField()
        end_time = models.TimeField()

    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    intructor = models.ForeignKey(Professor, null=False, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam_time = models.DateTimeField()
    schedule = models.ManyToManyField(Schedule)


class ClassEvent(Event):
    TYPE_CHOICES = [
        ("midterm", "Midterm Exam"),
        ("final", "Final Exam"),
        ("quiz", "Quiz"),
        ("project", "Project"),
    ]
    name = models.CharField(choices=TYPE_CHOICES, max_length=25)
    class_course = models.ForeignKey(Class, related_name="events", on_delete=models.CASCADE)


class Student(UserAccount):
    student_id = models.CharField(max_length=15, unique=True)
    advisor = models.ForeignKey(Advisor, on_delete=models.PROTECT)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_course = models.ForeignKey(Class, on_delete=models.CASCADE)
    grade = models.DecimalField(min=0, max=20, blank=True)


class AdvisingMessage(models.Model):
    content = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

# Notification
# System suggestion
#