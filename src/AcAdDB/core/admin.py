from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PhoneNumber)
admin.site.register(UserAccount)

admin.site.register(Major)
admin.site.register(Degree)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CoursePrerequisite)
admin.site.register(Chart)
admin.site.register(Term)
admin.site.register(Class)

admin.site.register(Event)
admin.site.register(TermEvent)
admin.site.register(ClassEvent)

admin.site.register(Professor)
admin.site.register(Advisor)
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(AdvisingMessage)
