from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from models import *
from requests import *


def select_user(username) -> UserAccount | Student | Professor | Advisor:
    user = User.objects.filter(username=username).first()
    if not user:
        return None
    return user.account


# Create your views here.
def student_information(re, s_id):
    student = Student.objects.filter(student_id=s_id).first()

    info = {"id": s_id, "name": student.get_full_name(), "major": student.educational_stat.major
            "grade": student.get_avg(), "advisor": student.advisor}

    return (
        render(
            re,
            {
            }
        )
    )
