import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from edu.models import EducationalStat, Department
class PhoneNumber(models.Model):
    PHONE_TYPES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"))
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=6, choices=PHONE_TYPES, default="Mobile")
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
    

    def clean(self):
        if not self.phone_numbers.filter(phone_type="Mobile").exists():
            raise ValidationError("One Phone number with type Mobile is required.")

    def get_age(self):
        """
        Calculate and return user age.
        """
        current_year = datetime.datetime.now().year
        birth_year = self.date_of_birth.year
        return current_year - birth_year

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
