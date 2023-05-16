from django.db import models
from django.contrib.auth.models import User
from django_better_admin_arrayfield.models.fields import ArrayField

from Tutors.models import Tutor

from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.

class InterviewStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolment_date = models.DateTimeField()
    tasks = ArrayField(
            models.CharField(max_length=100, blank=True),
            default=list,  # Add this line
        )
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # ucatClass = models.ManyToManyField('UcatClass', through='Enrollment')
    def __str__(self):
        return str(self.user)