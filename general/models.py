from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UcatStudent(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)


class UcatSection(models.Model):
    name = models.CharField(max_length=20)


class UcatSectionInstance(models.Model):
    student = models.ForeignKey(UcatStudent, on_delete=models.CASCADE)
    start_date = models.DateField()
    

class UcatVideo(models.Model):
    section = models.ForeignKey(UcatSection)
    url = models.URLField()