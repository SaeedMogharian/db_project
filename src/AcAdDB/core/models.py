import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PhoneNumber(models.Model):
    PHONE_TYPES = (("Mobile", "Mobile"), ("Work", "Work"), ("Home", "Home"))
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=6, choices=PHONE_TYPES, default="Mobile")


class Major(models.Model):
    name = models.CharField(max_length=255)
    requierd_credit = models.IntegerField()


class Degree(models.Model):
    D_CHOICES = [
        ("Bachelor", "Bachelor"),
        ("Master", "Master"),
        ("PhD", "PhD"),
    ]
    name = models.CharField(choices=D_CHOICES, max_length=10)


class Department(models.Model):
    name = models.CharField(max_length=255)


# EduStat
class UserAccount(models.Model):
    class Meta:
        verbose_name = "User"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")

    GENDER_TYPES = (("M", "Male"), ("F", "Female"))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=255)
    national_code = models.CharField(max_length=20, unique=True)
    phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)
    email_address = models.EmailField(max_length=254)
    address = models.CharField(max_length=1000)

    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    degree = models.ForeignKey(Degree, null=True, on_delete=models.SET_NULL)

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
        return f"Professor {str(self.get_full_name())}"


# department, major
class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    cred = models.IntegerField(default=1)
    cataloge = models.TextField()

    def __str__(self):
        return str(self.name)


class CoursePrerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    prerequisites = models.ManyToManyField(Course, related_name="pre_req")

    # check if unique
    # check if not precondition itself


class Chart(models.Model):
    major = models.OneToOneField(Major, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    common = models.ManyToManyField(Course)
    core = models.ManyToManyField(Course)
    optional = models.ManyToManyField(Course)
    general = models.ManyToManyField(Course)

    def r_term(self):
        if self.degree == "Bachelor":
            return 8
        elif self.degree == "Master":
            return 4
        else:
            return 6


# department
class Professor(models.Model):
    class Meta:
        verbose_name = "professor"

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


class Event(models.Model):
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)


class Term(models.Model):
    number = models.CharField(unique=True, primary_key=True)

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
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="term")
    name = models.CharField(choices=TYPE_CHOICES, max_length=25)
    term = models.ForeignKey(Term, related_name="events", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' for this term'


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


# Student
class Student(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="student")
    s_id = models.CharField(max_length=15, unique=True)
    advisor = models.ForeignKey(Advisor, null=True, on_delete=models.SET_NULL)
    entery_term = models.ForeignKey(Term, null=True, on_delete=models.SET_NULL)

    def get_enrolls(self, term_number=None):
        if term_number:
            return self.enrollments.filter(class_course__term__number=term_number).all()
        return self.enrollments.all()

    def get_avg(self, term_number=None):
        en = self.get_enrolls(term_number=term_number)
        g = list(en.values_list("grade", flat=True))
        return sum(g) / len(g)

    def advisor_messages(self, advisor_id):
        return self.messages.filter(student=self, advisor__a_id=advisor_id)

    def get_events(self, term_number):
        # ev = []
        # term = Term.objects.filter(term_number=term_number).first()
        # ev += term.events.all()
        enrolls = self.get_enrolls(term_number).values_list("class_course")
        # for x in enrolls:
        #     ev += x.class_course.events.all()
        ev = Event.objects.filter(term__term__number=term_number).all() | Event.objects.filter(
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

    def term_count(self, curr_num):
        curr = Term.objects.filter(number=curr_num).first()
        return Term.terms_between(self.entery_term, curr)

    def cred_behind(self, term_num):
        cred_avg = self.account.major.requierd_credit // self.account.major.chart.r_term()
        term_count = len(self.term_count(term_num))
        return self.pass_cred_count() - cred_avg * term_count

    def possible_takes(self, term_num):
        chart = self.account.major.chart
        taken = self.passed_course()
        curr = list(self.get_enrolls(term_num))
        po = []
        al = chart.core.all() | chart.common.all() | chart.general.all() | chart.optional.all()
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

    def __str__(self):
        return str(self.account)


# Student, Class(term, course, professor)
class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    class_course = models.ForeignKey(Class, related_name="enrollments", on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True)


class AdvisingMessage(models.Model):
    content = models.TextField()
    student = models.ForeignKey(Student, related_name="messages", on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, related_name="messages", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    Sender_Choice = [("s", "Student"), ("a", "Advisor")]
    sender = models.CharField(choices=Sender_Choice, max_length=10)

# Notification
# System suggestion
#
