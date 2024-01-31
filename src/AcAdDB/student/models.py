from django.db import models

# Create your models here.
from core.models import UserAccount

class Student(UserAccount):
    student_id = models.CharField(max_length=15, unique=True)
    
    # Add other student-related fields

# Add more student-related models as needed
