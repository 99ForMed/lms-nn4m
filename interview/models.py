from django.db import models
from django.contrib.auth.models import User
from django_better_admin_arrayfield.models.fields import ArrayField

from Tutors.models import Tutor

from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.

class InterviewClass(models.Model):
    name = models.CharField(max_length=200)
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True)  # Added tutor field
    def __str__(self):    
        return self.name

class InterviewStudent(models.Model):

    interview_class = models.ForeignKey(InterviewClass, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zoom_access_token = models.TextField(null=True, blank=True)
    zoom_refresh_token = models.TextField(null=True, blank=True)
    zoom_token_expiration = models.DateTimeField(null=True, blank=True)
    enrolment_date = models.DateTimeField(null=True, blank=True)
    tasks = ArrayField(
            models.CharField(max_length=100, blank=True),
            default=list,
        )
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return str(self.user)
