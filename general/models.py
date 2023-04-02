from django.db import models
from django.contrib.auth.models import User
from django_better_admin_arrayfield.models.fields import ArrayField

from Tutors.models import Tutor

from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
# Create your models here.

class UcatStudent(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    enrolment_date = models.DateTimeField()
    tasks = ArrayField(
            models.CharField(max_length=100, blank=True),
            default=list,  # Add this line
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
    
@receiver(post_save, sender=User)
def create_ucat_student_and_section(sender, instance, created, **kwargs):
    if created:  # If it's a new user
        new_student = UcatStudent.objects.create(user=instance, enrolment_date=datetime.datetime.now())
        # Add your logic to get the UcatSection you want to create a UcatSectionInstance for
        ucat_section = UcatSection.objects.all()[0]  # Replace 'some_id' with the actual ID or filter conditions
        UcatSectionInstance.objects.create(student=new_student, section=ucat_section, start_date=datetime.datetime.now().date(), current=True, skills_mastered=0)