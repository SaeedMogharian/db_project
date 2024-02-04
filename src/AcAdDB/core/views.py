# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
def first_page(request):
    return (
        render(
            request,
            "index.html"
        )
    )


def login_page(request):
    # handle login
    # TODO: login with student code and advisor code
    if request.method == "POST":
        if 'login_form' in request.POST:
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user:
                login(request, user)
                if hasattr(user.account, 'student'):
                    return redirect('student_dashboard_link')
                elif hasattr(user.account, 'professor'):
                    if hasattr(user.account.professor, 'advisor'):
                        return redirect('advisor_dashboard_link')
            else:
                raise Http404("User Not Found")

    user = select_user(request.user)
    if hasattr(user, 'student'):
        return redirect('student_dashboard_link')
    elif hasattr(user, 'professor'):
        if hasattr(user.professor, 'advisor'):
            return redirect('advisor_dashboard_link')
    return (
        render(
            request,
            "login.html"
        )
    )


# TODO: forgot password


# def signup_page(re):
#     pass


# Both
def messaging(request, a_id, s_id):
    user = select_user(request.user)
    if not user:
        return redirect('first_page_link')
    if not hasattr(user, "professor") and not hasattr(user, "student"):
        return redirect('first_page_link')
    if hasattr(user, "professor") and not hasattr(user.professor, "advisor"):
        return redirect('first_page_link')
    student = Student.objects.filter(s_id=str(s_id)).first()
    advisor = Advisor.objects.filter(a_id=str(a_id)).first()
    if not student or not advisor:
        return redirect('first_page_link')
    if not hasattr(user, "professor"):
        me = "student"
    else:
        me = "advisor"

    if request.method == "POST":
        if 'send_message' in request.POST:
            AdvisingMessage.objects.create(
                content=request.POST['message'],
                advisor=advisor,
                student=student,
                sender=me
            )
            return redirect("messaging_link", a_id, s_id)


    messages = AdvisingMessage.objects.filter(student__s_id=s_id, advisor__a_id=a_id).all().order_by("created_time")
    return (
        render(
            request,
            "messaging.html",
            {
                "s_id": s_id,
                "s_name": student.account.get_full_name(),
                "a_id": a_id,
                "a_name": advisor.professor.account.get_full_name(),
                "me": me,
                "messages": messages,
            }
        )
    )


# Student
def student_dashboard(request):
    user = select_user(request.user)
    if not hasattr(user, "student"):
        return redirect('first_page_link')
    student = user.student
    # chart avg_grade of each term
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    t_avg = {}
    for i in terms:
        t_avg[i] = student.get_avg(i)
    # calendar view
    events = student.get_events(CURRENT_TERM_NUMBER)
    date = datetime.datetime.now().date()
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
            request,
            "student_dashboard.html",
            {
                "s_id": str(student.s_id),
                "a_id": str(student.advisor.a_id),
                "student": student.account.get_full_name(),
                "chart": t_avg,
                "date": date,
                "alert": alert,
                "t_count": t_count,
                "cred_behind": cred_behind,
                "possibles": possibles
            }
        )
    )


def student_info(request):
    student = select_user(request.user).student
    if not student:
        return redirect('first_page_link')

    info = {"s_id": student.s_id, "name": student.account.get_full_name(),
            "major": student.account.major,
            "grade": student.get_avg(), "advisor": student.advisor,
            "cred": student.pass_cred_count()}
    enrolls = {}
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    for i in terms:
        enrolls[i] = student.passed_course(i.number)

    failed_terms = student.get_failed_terms()
    return (
        render(
            request,
            "student_info.html",
            {
                "s_id": str(student.s_id),
                "a_id": str(student.advisor.a_id),
                "info": info,
                "enrolls": enrolls,
                "failed_terms": failed_terms
            }
        )
    )


# Advisor
def advisor_dashboard(request):
    user = select_user(request.user)
    if not hasattr(user, "professor"):
        return redirect('first_page_link')
    elif not hasattr(user.professor, "advisor"):
        return redirect('first_page_link')
    advisor = user.professor.advisor
    # table of students with over all view of their stat
    students = advisor.student_set.all()

    # Term Events
    t_event = Event.objects.filter(term_event__term__number=CURRENT_TERM_NUMBER).all()

    return (
        render(
            request,
            "advisor_dashboard.html",
            {
                "a_id": advisor.a_id,
                "advisor": advisor.professor.account.get_full_name(),
                "events": t_event,
                "students": students
            }
        )
    )


def advisor_profile(request):
    user = select_user(request.user)
    if not hasattr(user, "professor"):
        return redirect('first_page_link')
    elif not hasattr(user.professor, "advisor"):
        return redirect('first_page_link')
    advisor = user.professor.advisor

    info = {"a_id": advisor.a_id, "name": advisor.professor.account.get_full_name(),
            "major": advisor.professor.account.major}

    students = len(list(advisor.student_set.all()))
    return (
        render(
            request,
            "advisor_profile.html",
            {
                "info": info,
                "student_count": students
            }
        )
    )


def advising_student(request, s_id):
    user = select_user(request.user)
    if not hasattr(user, "professor"):
        return redirect('first_page_link')
    elif not hasattr(user.professor, "advisor"):
        return redirect('first_page_link')
    advisor = user.professor.advisor
    # student info
    student = Student.objects.filter(s_id=s_id).first()
    if not advisor.student_set.filter(s_id=s_id):
        return redirect('first_page_link')

    info = {"s_id": student.s_id, "name": student.account.get_full_name(),
            "major": student.account.major,
            "grade": student.get_avg(), "advisor": student.advisor,
            "cred": student.pass_cred_count()}
    enrolls = {}
    terms = list(Term.objects.filter(number__gte=student.entery_term, number__lte=CURRENT_TERM_NUMBER))
    for i in terms:
        enrolls[i] = student.passed_course(i.number)
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
    date = datetime.datetime.now().date()
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
            request,
            "advising_student.html",
            {
                "advisor": advisor,
                "student": student,
                "info": info,
                "enrolls": enrolls,
                "t_avg": t_avg,
                "date": date,
                "alert": alert,
                "t_count": t_count,
                "cred_behind": cred_behind,
                "possibles": possibles,
                "failed_terms": failed_terms
            }
        )
    )


def logout_view(request):
    logout(request)
    return redirect("first_page_link")
