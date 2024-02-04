# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import Http404

from .models import *

CURRENT_TERM_NUMBER = "14021"


def select_user(username) -> UserAccount:
    user = User.objects.filter(username=username).first()
    if hasattr(user, "account"):
        return user.account
    return None


# Create your views here.

# UserAccount
def first_page(re):
    return (
        render(
            re,
            "index.html"
        )
    )


def login_page(re):
    # handle login
    if re.method == "POST":
        if 'login_form' in re.POST:
            user = authenticate(
                username=re.POST['email'],
                password=re.POST['password']
            )
            if user and user.is_active:
                login(re, user)
                return redirect('login_page_link')
            raise Http404("User Not Found")

    user = select_user(re.user)
    if hasattr(user, 'student'):
        return redirect('student_dashboard_link')
    elif hasattr(user, 'professor'):
        if hasattr(user.professor, 'advisor'):
            return redirect('advisor_dashboard_link')
    return (
        render(
            re,
            "login.html"
        )
    )


# TODO: forgot password


def signup_page(re):
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
    user = select_user(re.user)
    # if not hasattr(user, "student"):
    #     return redirect('first_page_link')
    student = user.student
    # chart avg_grade of each term
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    t_avg = {}
    for i in terms:
        t_avg[i] = student.get_avg(i)
    # calendar view
    events = student.get_events(CURRENT_TERM_NUMBER)
    date = datetime.datetime.now()
    # events alert
    alert = {}
    for e in events.iterator():
        if e.start > date and (e.end.day - date.day) < 10:
            if e.class_course:
                alert[e] = f"{str(e.class_course)} is very close"
            elif e.term:
                alert[e] = f"{str(e.term.term)} is very close"

    # recommendation for next term
    t_count = student.term_count()
    cred_behind = student.cred_behind()
    possibles = student.possible_takes(CURRENT_TERM_NUMBER)

    # send message to advisor link
    # student info link
    # student all calendar link

    return (
        render(
            re,
            "student_dashboard.html",
            {
                "chart": t_avg,
                "events": events,
                "date": date,
                "alert": alert,
                "t_count": t_count,
                "cred_behind": cred_behind,
                "possibles": possibles
            }
        )
    )


def student_info(re):
    student = select_user(re.user).student
    if not student:
        return redirect('first_page_link')

    info = {"s_id": student.s_id, "name": student.account.get_full_name(),
            "major": student.account.major,
            "grade": student.get_avg(), "advisor": student.advisor,
            "cred": student.pass_cred_count()}
    enrolls = {}
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    for i in terms:
        enrolls[i] = student.get_enrolls(i.number)

    failed_terms = student.get_failed_terms()
    return (
        render(
            re,
            # student information template
            {
                "info": info,
                "enrolls": enrolls,
                "failed_terms": failed_terms
            }
        )
    )


def student_calendar(re):
    student = select_user(re.user).student
    if not student:
        return redirect('first_page_link')

    events = student.get_events(CURRENT_TERM_NUMBER)
    date = datetime.datetime.now()
    return (
        render(
            re,
            # student information template
            {
                "events": events,
                "date": date
            }
        )
    )


# Advisor
def advisor_dashboard(re):
    advisor = select_user(re.user).professor.advisor
    if not advisor:
        return redirect('first_page_link')
    # table of students with over all view of their stat
    students = advisor.student_set.all()

    # Term Events
    t_event = Event.objects.filter(term__term__number=CURRENT_TERM_NUMBER).all()

    return (
        render(
            re,
            # advisor profile template
            {
                "events": t_event,
                "students": students
            }
        )
    )


def advisor_profile(re):
    advisor = select_user(re.user).professor.advisor
    if not advisor:
        return redirect('first_page_link')

    info = {"s_id": advisor.a_id, "name": advisor.professor.account.get_full_name(),
            "major": advisor.professor.account.major,
            "degree": advisor.professor.account.degree}

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
    advisor = select_user(re.user).professor.advisor
    if not advisor:
        return redirect('first_page_link')
    # student info
    student = Student.objects.filter(s_id=s_id)
    info = {"s_id": student.s_id, "name": student.account.get_full_name(),
            "major": student.account.major,
            "grade": student.get_avg(), "advisor": student.advisor,
            "cred": student.pass_cred_count()}
    enrolls = {}
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    for i in terms:
        enrolls[i] = student.get_enrolls(i.number)
    failed_terms = student.get_failed_terms()
    # chart of students
    # student event
    # system recommendation for next term
    # chart avg_grade of each term
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    t_avg = {}
    for i in terms:
        t_avg[i] = student.get_avg(i.number)
    # calendar view
    events = student.get_events(CURRENT_TERM_NUMBER)
    date = datetime.datetime.now()
    # events alert
    alert = {}
    for e in events.iterator():
        if e.start > date and (e.end.day - date.day) < 10:
            if e.class_course:
                alert[e] = f"{str(e.class_course)} is very close"
            elif e.term:
                alert[e] = f"{str(e.term.term)} is very close"

    # recommendation for next term
    t_count = student.term_count()
    cred_behind = student.cred_behind()
    possibles = student.possible_takes(CURRENT_TERM_NUMBER)

    # send message link
    return (
        render(
            re,
            # advisor profile template
            {
                "info": info,
                "enrolls": enrolls,
                "t_avg": t_avg,
                "events": events,
                "date": date,
                "alert": alert,
                "t_count": t_count,
                "cred_behind": cred_behind,
                "possibles": possibles,
                "failed_terms": failed_terms
            }
        )
    )
