import termios

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from requests import *

CURRENT_TERM_NUMBER = 4022


def select_user(username) -> UserAccount:
    user = User.objects.filter(username=username).first()
    if isinstance(user, Advisor):
        return None
    return user.account


# Create your views here.

# UserAccount
def first_page(re):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def forgot_password(re):
    pass


# Both
def messaging(re, a_id, s_id):
    user = select_user(re.user)
    if not user:
        return redirect('first_page_link')
    student = Student.objects.filter(s_id=s_id)
    advisor = Advisor.objects.filter(a_id=a_id)
    if not student and not advisor:
        pass
    messages = AdvisingMessage.objects.filter(student=student, advisor=advisor)

    return (
        render(
            re,
            # messaging template
            {
                "messages": messages,
            }
        )
    )


# Student
def student_dashboard(re):
    pass


def student_info(re):
    student = select_user(re.user).student
    if not student:
        return redirect('first_page_link')

    info = {"s_id": student.s_id, "name": student.account.get_full_name(),
            "major": student.account.educational_stat.major,
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


def student_calendar(re):
    student = select_user(re.user).student
    if not student:
        return redirect('first_page_link')

    events = student.get_events(CURRENT_TERM_NUMBER)
    return (
        render(
            re,
            # student information template
            {
                "events": events,
            }
        )
    )


# Advisor
def advisor_dashboard(re):
    pass


def advisor_profile(re):
    advisor = select_user(re.user).professor.advisor
    if not advisor:
        return redirect('first_page_link')

    info = {"s_id": advisor.a_id, "name": advisor.professor.account.get_full_name(),
            "major": advisor.professor.account.educational_stat.major,
            "degree": advisor.professor.account.educational_stat.degree,
            "inst_name": advisor.professor.account.educational_stat.institution_name}

    students = advisor.student_set.all()
    return (
        render(
            re,
            # advisor profile template
            {
                "info": info,
                "students": students
            }
        )
    )


def advising_student(re, s_id):
    pass
