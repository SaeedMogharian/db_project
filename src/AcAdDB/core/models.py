import datetime

from django.db import models
from django.contrib.auth.models import User


# from django.core.exceptions import ValidationError
Degree_CHOICES = [
        ("Bachelor", "Bachelor"),
        ("Master", "Master"),
        ("PhD", "PhD"),
]

class PhoneNumber(models.Model):
    PHONE_TYPES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"))
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=6, choices=PHONE_TYPES, default="Mobile")

    class Meta:
        verbose_name = 'PhoneNumber'
        verbose_name_plural = "Core | PhoneNumbers"


class Major(models.Model):
    name = models.CharField(max_length=255)
    requierd_credit = models.IntegerField()

    class Meta:
        verbose_name = 'Major'
        verbose_name_plural = "Edu | Majors"
    
    def __str__(self):
        return str(self.name)


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = "Edu | Departments"


# EduStat
class UserAccount(models.Model):
    class Meta:
        verbose_name = "UserAccount"
        verbose_name_plural = "Core | UserAccounts"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")

    GENDER_TYPES = (("M", "Male"), ("F", "Female"))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=255)
    national_code = models.CharField(max_length=20, unique=True)
    phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)
    address = models.CharField(max_length=1000)

    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.SET_NULL)
    degree = models.CharField(choices=Degree_CHOICES, null=True, blank=True, max_length=10)

    def get_age(self):
        """
        Calculate and return user age.
        """
        current_year = datetime.datetime.now()
        birth_year = self.date_of_birth.year
        return current_year - birth_year

    def get_full_name(self):
        """
        Return the first_name and last_name.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{str(self.get_full_name())}"


# department, major
class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    cred = models.IntegerField(default=1)
    cataloge = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = "Edu | Course"


class CoursePrerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    prerequisites = models.ManyToManyField(Course, related_name="pre_req")

    class Meta:
        verbose_name = 'Prerequisite'
        verbose_name_plural = "Edu | Prerequisites"

    # check if unique
    # check if not precondition itself


class Chart(models.Model):
    major = models.OneToOneField(Major, on_delete=models.CASCADE)
    degree = models.CharField(choices=Degree_CHOICES, max_length=10)
    courses = models.ManyToManyField(Course, related_name="chart")

    def r_term(self):
        if self.degree == "Bachelor":
            return 8
        elif self.degree == "Master":
            return 4
        else:
            return 6

    class Meta:
        verbose_name = 'Chart'
        verbose_name_plural = "Edu | Charts"


# department
class Professor(models.Model):
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = "Users | Professors"

    RANK_CHOICES = [
        ("Instructor", "Instructor"),
        ("Assistant Professor", "Assistant Professor"),
        ("Associative Professor", "Associative Professor"),
        ("Full Professor", "Full Professor"),
    ]
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="professor")
    rank = models.CharField(max_length=255, choices=RANK_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"Professor {str(self.account)}"


class Advisor(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE, related_name="advisor")
    a_id = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"Advisor {str(self.professor)}"

    class Meta:
        verbose_name = 'Advisor'
        verbose_name_plural = "Users | AdvisorProfessors"


class Event(models.Model):
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = "Core | Events"

    def __str__(self):
        if hasattr(self, "term"):
            return str(self.term_event)
        elif hasattr(self, "class_course"):
            return str(self.class_course)


class Term(models.Model):
    number = models.CharField(unique=True, primary_key=True, max_length=6)

    # year|term_num
    def get_term_events(self):
        return self.events.all()

    def next_term_num(self, summer=False):
        n = self.number
        if n[-1] == "3":
            return str(int(n[:-1]) + 1) + "1"
        if n[-1] == "2":
            if summer:
                return str(int(n[:-1])) + "3"
            else:
                return str(int(n[:-1]) + 1) + "1"
        if n[-1] == "1":
            return str(int(n[:-1])) + "2"

    @staticmethod
    def terms_between(start, end):
        if int(start.number) > int(end.number):
            start, end = end, start
        terms = []
        x = start
        while x.number != str(end.number):
            terms.append(x.number)
            x = x.next_term_num()

        return terms

    class Meta:
        verbose_name = 'Term'
        verbose_name_plural = "Edu | Terms"

    def __str__(self):
        return str(self.number)


# term
class TermEvent(models.Model):
    TYPE_CHOICES = [
        ("preregister", "preregister"),
        ("term", "Term"),
        ("class", "Class"),
        ("register", "Register"),
        ("adjustment", "Adjustment"),
        ("drop", "Drop"),
        ("exams", "Exams"),
    ]
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="term_event")
    name = models.CharField(choices=TYPE_CHOICES, max_length=25)
    term = models.ForeignKey(Term, related_name="events", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TermEvent'
        verbose_name_plural = "Core | TermEvents"

    def __str__(self):
        return str(self.name)

# term , course, Professor
class Class(models.Model):
    class Schedule(models.Model):
        DAY_CHOICES = [
            ("Sat", "Saturday"),
            ("Sun", "Sunday"),
            ("Mon", "Monday"),
            ("Tue", "Tuesday"),
            ("Wed", "Wednesday"),
            ("Thu", "Thursday"),
            ("Fri", "Friday"),
        ]
        weekday = models.CharField(choices=DAY_CHOICES, max_length=10)
        start_time = models.TimeField()
        end_time = models.TimeField()

    course = models.ForeignKey(Course, null=False, related_name="classes", on_delete=models.CASCADE)
    intructor = models.ForeignKey(Professor, null=False, related_name="classes", on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="classes")
    exam_time = models.DateTimeField()
    schedule = models.ManyToManyField(Schedule)

    def __str__(self):
        return str(self.course) + ' | ' + str(self.intructor)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = "Edu | Class"


# class
class ClassEvent(models.Model):
    TYPE_CHOICES = [
        ("midterm", "Midterm Exam"),
        ("final", "Final Exam"),
        ("quiz", "Quiz"),
        ("project", "Project"),
    ]
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="class_course")
    name = models.CharField(choices=TYPE_CHOICES, max_length=25)
    class_course = models.ForeignKey(Class, related_name="events", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' for ' + str(self.class_course)

    class Meta:
        verbose_name = 'ClassEvent'
        verbose_name_plural = "Core | ClassEvents"


# Student
class Student(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="student")
    s_id = models.CharField(max_length=15, unique=True)
    advisor = models.ForeignKey(Advisor, null=True, blank=True, on_delete=models.SET_NULL)
    entery_term = models.ForeignKey(Term, null=True, blank=True, on_delete=models.SET_NULL)

    def get_enrolls(self, term_number=None):
        if term_number:
            return self.enrollments.filter(class_course__term__number=term_number).all()
        return self.enrollments.all()

    def get_avg(self, term_number=None):
        en = self.get_enrolls(term_number=term_number)
        g = list(en.values_list("grade", flat=True))
        if len(g)!=0:
            return sum(g) / len(g)
        return 0

    def advisor_messages(self, advisor_id):
        return self.messages.filter(student=self, advisor__a_id=advisor_id)

    def get_events(self, term_number):
        # ev = []
        # term = Term.objects.filter(term_number=term_number).first()
        # ev += term.events.all()
        enrolls = self.get_enrolls(term_number).values_list("class_course")
        # for x in enrolls:
        #     ev += x.class_course.events.all()
        ev = Event.objects.filter(term_event__term__number=term_number).all() | Event.objects.filter(
            class_course__class_course__in=enrolls)
        return ev

    def cred_count(self, term_number=None):
        en = self.get_enrolls(term_number)
        c = 0
        for x in en:
            c += x.class_course.course.cred
        return c

    def fail_cred_count(self, term_number=None):
        en = self.get_enrolls(term_number).filter(grade__lt=10)
        c = 0
        for x in en:
            c += x.class_course.course.cred
        return c

    def pass_cred_count(self, term_number=None):
        return self.cred_count(term_number) - self.fail_cred_count(term_number)

    def passed_course(self, term_number=None):
        enrolls = self.get_enrolls(term_number)
        c = []
        for x in enrolls:
            if x.grade >= 10:
                c.append(x.class_course.course)
        return c

    def term_count(self):
        curr = Term.objects.filter(number=self.last_term()).first()
        return Term.terms_between(self.entery_term, curr)

    def cred_behind(self):
        cred_avg = self.account.major.requierd_credit // self.account.major.chart.r_term()
        term_count = len(self.term_count())
        return self.pass_cred_count() - cred_avg * term_count

    def possible_takes(self, term_num):
        chart = self.account.major.chart
        taken = self.passed_course()
        curr = list(self.get_enrolls(term_num))
        po = []
        al = chart.courses.all()
        for x in al.iterator():
            if x not in taken and x not in curr:
                pre_sat = True
                for a in x.pre_req.all():
                    if a not in taken:
                        pre_sat = False
                        break
                if pre_sat:
                    po.append(x)
        return po

    def last_term(self):
        e = self.enrollments.all()
        t = int(self.entery_term.number)
        for i in e:
            if int(i.class_course.term.number) > t:
                t = int(i.class_course.term.number)
        return t

    def get_failed_terms(self):
        failed_t = []
        terms = list(Term.objects.filter(number__gte=self.entery_term, number__lte=self.last_term()))
        for i in terms:
            if self.get_avg(i) < 12:
                failed_t.append(i.number)
        return failed_t

    def __str__(self):
        return str(self.account)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = "Users | Students"


# Student, Class(term, course, professor)
class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    class_course = models.ForeignKey(Class, related_name="enrollments", on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'Enrolls'
        verbose_name_plural = "Users | StudentEnrollment"


class AdvisingMessage(models.Model):
    content = models.TextField()
    student = models.ForeignKey(Student, related_name="messages", on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, related_name="messages", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    Sender_Choice = [("student", "Student"), ("advisor", "Advisor")]
    sender = models.CharField(choices=Sender_Choice, max_length=10)

    class Meta:
        verbose_name = 'Core'
        verbose_name_plural = "Core | AdvisingMessages"
# Notification
# System suggestion
#
