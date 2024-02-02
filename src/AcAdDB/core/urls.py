from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import *


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout_link'),
    path("", first_page, name="first_page_link"),
    # forgot pass
    path("student/", student_dashboard, name="student_dashboard_link"),
    path("student/inforamtion/", student_info, name="student_info_link"),
    path("student/calendar/", student_calendar, name="student_calendar_link"),

    path("advisor/", advisor_dashboard, name="advisor_dashboard_link"),
    path("advisor/profile/", advisor_profile, name="advisor_profile_link"),
    path("advisor/students/<str:s_id>/", advising_student, name="advising_student_link"),

    path("messaging/<str:a_id>+<str:s_id>/", advising_student, name="advising_student_link"),
]