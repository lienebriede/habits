from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=50)

    def __str__(self):
        return self.name
