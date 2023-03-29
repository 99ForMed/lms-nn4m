from django.db import models
from django.contrib.auth.models import User
from django_better_admin_arrayfield.models.fields import ArrayField

from Tutors.models import Tutor
# Create your models here.

class UcatStudent(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    enrolment_date = models.DateTimeField()
    tasks = ArrayField(
            models.CharField(max_length=100, blank=True)
        )
    ucatClass = models.ManyToManyField('UcatClass', through='Enrollment')
    def __str__(self):
        return str(self.user)


class UcatSection(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
            return str(self.name)

class UcatSectionInstance(models.Model):
    student = models.ForeignKey(UcatStudent, on_delete=models.CASCADE)
    section = models.ForeignKey(UcatSection, on_delete=models.CASCADE)
    start_date = models.DateField()
    current = models.BooleanField()
    skills_mastered = models.IntegerField()

    def __str__(self):
        return str(self.section) +" - "+ str(self.student)
    

class UcatVideo(models.Model):
    section = models.ForeignKey(UcatSection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=50)
    unlocked = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class UcatClass(models.Model):
    name = models.CharField(max_length=100)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True, related_name='classes')
    students = models.ManyToManyField('UcatStudent', through='Enrollment')
    class_notes = models.TextField()

    def __str__(self):
        return str(self.name) + " taught by " + str(self.tutor)

class Enrollment(models.Model):
    student = models.ForeignKey(UcatStudent, on_delete=models.CASCADE)
    UcatClass = models.ForeignKey(UcatClass, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.student) + " - " + str(self.UcatClass)
    
class UcatProblem(models.Model):
    student = models.ForeignKey(UcatStudent, on_delete=models.CASCADE, related_name='UcatProblems')
    video = models.ForeignKey(UcatVideo, on_delete=models.CASCADE, related_name='UcatProblems')
    problem = models.TextField()
    solved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student)+ " - " + str(self.problem)