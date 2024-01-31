from django.db import models

from edu.models import Department, Course
from core.models import UserAccount
# Create your models here.
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
    intsructed_courses = models.ManyToManyField(Course, on_delete=models.CASCADE, blank= True)

class Advisor(Professor):
    advisor_id = models.CharField(max_length=15, unique=True)