from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UcatStudent(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    enrolment_date = models.DateTimeField()
    

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
    name = models.CharField(max_length=30)
    description = models.TextField()
    thumbnail = models.ImageField(null = True)
    url = models.CharField(max_length=50)
    unlocked = models.BooleanField(default=False)


    def __str__(self):
        return self.name