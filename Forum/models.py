from django.db import models
from django.contrib.auth.models import User

from general.models import UcatVideo



# Create your models here.

class Comment(models.Model):
    forum = models.ForeignKey(UcatVideo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return str(self.user) + " - \"" + str(self.content)+"\""

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return str(self.user) + " - \"" + str(self.content)+"\""