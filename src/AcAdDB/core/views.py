import termios

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from models import *
from requests import *

CURRENT_TERM_NUMBER = 4022


def select_user(username) -> UserAccount | Student | Professor | Advisor:
    user = User.objects.filter(username=username).first()
    if not user:
        return None
    return user.account


# Create your views here.
def student_information(re, s_id):
    # user = select_user(re.user)
    # if not user:
    #     return redirect('landing_page_link')

    student = Student.objects.filter(s_id=s_id).first()

    info = {"s_id": s_id, "name": student.get_full_name(), "major": student.educational_stat.major,
            "grade": student.get_avg(), "advisor": student.advisor,
            "cred": student.cred_count() - student.fail_cred_count()}

    enrolls = {}
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    for i in terms:
        enrolls[i] = student.get_enrolls(i)
    return (
        render(
            re,
            # student information template
            {
                "info": info,
                "enrolls": enrolls
            }
        )
    )
