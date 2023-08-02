from django.db import models
from django.contrib.auth.models import User
from general.models import *

class Tutor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zoom_access_token = models.TextField(blank=True, null=True)
    zoom_refresh_token = models.TextField(blank=True, null=True)
    zoom_token_expiration = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user)
