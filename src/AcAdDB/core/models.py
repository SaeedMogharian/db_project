import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PhoneNumber(models.Model):
    PHONE_TYPES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"))
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=6, choices=PHONE_TYPES, default="Mobile")


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


class CoursePrecondition(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    precondition = models.ManyToManyField(Course, on_delete=models.CASCADE)

    # check if unique
    # check if not precondition itself


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


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
    picture = models.ImageField(upload_to="images/")
    address = models.CharField(max_length=255)

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


class Student(UserAccount):
    student_id = models.CharField(max_length=15, unique=True)


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
    intsructed_courses = models.ManyToManyField(Course, on_delete=models.CASCADE, blank=True)


class Advisor(Professor):
    advisor_id = models.CharField(max_length=15, unique=True)


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
        weekday = models.Choices(choices=DAY_CHOICES)
        start_time = models.TimeField()
        end_time = models.TimeField()

    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    intructor = models.ForeignKey(Professor, null=False, on_delete=models.CASCADE)
    schedule = models.ManyToManyField(Schedule, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_course = models.ForeignKey(Class, on_delete=models.CASCADE)
    # Add other fields as needed


class AdvisingNote(models.Model):
    content = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed
