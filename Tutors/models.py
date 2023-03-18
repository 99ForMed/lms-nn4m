from django.db import models
from django.contrib.auth.models import User

from general.models import *

# Create your models here.

class Tutor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user)