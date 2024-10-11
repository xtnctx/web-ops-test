from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class ToDoModel(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    todo = models.CharField(max_length=200)



    def __str__(self) -> str:
        return self.user.username
    