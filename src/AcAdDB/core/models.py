# import datetime

# from django.db import models
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError


# class Address(models.Model):
#     state = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     street = models.CharField(max_length=255)
#     street_number = models.IntegerField()
#     building_name = models.CharField(max_length=255, blank=True)
#     district = models.CharField(max_length=255)
#     floor = models.IntegerField()
#     unit_number = models.IntegerField()
#     plate_number = models.CharField(max_length=10)
#     postal_code = models.CharField(max_length=20)
#     coordinate = models.CharField(max_length=255)
#     note = models.TextField(null=True, blank=True)


# class Education(models.Model):
#     start_date = models.DateField()
#     graduation_date = models.DateField()
#     major = models.CharField(max_length=255)
#     degree = models.CharField(max_length=255)
#     gpa = models.DecimalField(max_digits=5, decimal_places=2)
#     institution_name = models.CharField(max_length=255)
#     institution_address = models.ForeignKey(Address, on_delete=models.CASCADE)


# class PhoneNumber(models.Model):
#     PHONE_TYPES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"))
#     phone_number = models.CharField(max_length=20)
#     phone_type = models.CharField(max_length=6, choices=PHONE_TYPES, default="Mobile")


# class UserAccount(models.Model):
#     class Meta:
#         verbose_name = "Person"

#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     GENDER_TYPES = (("M", "Male"), ("F", "Female"))
#     persian_first_name = models.CharField(max_length=255)
#     persian_last_name = models.CharField(max_length=255)
#     gender = models.CharField(max_length=1, choices=GENDER_TYPES)
#     date_of_birth = models.DateField(null=True)
#     nationality = models.CharField(
#         max_length=255,
#     )
#     national_code = models.CharField(max_length=20, unique=True)
#     picture = models.ImageField(upload_to="images/")
#     home_address = models.ForeignKey(
#         Address, on_delete=models.SET_NULL, blank=True, null=True
#     )
#     educations = models.ManyToManyField(Education, blank=True)
#     phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)

#     # def clean(self):
#     #     if not self.phone_numbers.filter(phone_type="Mobile").exists():
#     #         raise ValidationError("One Phone number with type Mobile is required.")

#     def get_age(self):
#         """
#         Calculate and return user age.
#         """
#         current_year = datetime.datetime.now().year
#         birth_year = self.date_of_birth.year
#         return current_year - birth_year

#     def get_persian_first_name(self):
#         """
#         Return the persian_first_name.
#         """
#         return self.persian_first_name

#     def get_persian_last_name(self):
#         """
#         Return the persian_last_name.
#         """
#         return self.persian_last_name

#     def get_persian_full_name(self):
#         """
#         Return the persian_first_name and persian_last_name.
#         """
#         return f"{self.persian_first_name} {self.persian_last_name}"

# class Department(models.Model):
#     name = models.CharField(max_length=255)
#     budget = models.IntegerField()
#     creation_date = models.DateField()

# class Field(models.Model):
#     name = models.CharField(max_length=255)
#     department = models.ForeignKey(
#         Department, on_delete=models.CASCADE, related_name="fields"
#     )
#     head = models.OneToOneField(
#         "Professor", on_delete=models.SET_NULL, null=True, related_name="head_of_field"
#     )

# class Professor(models.Model):
#     class Meta:
#         verbose_name = "Professor"

#     RANK_CHOICES = [
#         ("Instructor", "Instructor"),
#         ("Assistant Professor", "Assistant Professor"),
#         ("Associative Professor", "Associative Professor"),
#         ("Full Professor", "Full Professor"),
#     ]
#     rank = models.CharField(max_length=255, choices=RANK_CHOICES)
#     field = models.ForeignKey(Field, on_delete=models.CASCADE)
#     is_in_committee = models.BooleanField(default=False)


# class Schedule(models.Model):
#     DAY_CHOICES = [
#         ("Sat", "Saturday"),
#         ("Sun", "Sunday"),
#         ("Mon", "Monday"),
#         ("Tue", "Tuesday"),
#         ("Wed", "Wednesday"),
#         ("Thu", "Thursday"),
#         ("Fri", "Friday"),
#     ]
#     day = models.CharField(choices=DAY_CHOICES, max_length=10)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
