from django.db import models
from django.contrib.auth.models import User

class HabitStacking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit1 = models.CharField(max_length=255)
    habit2 = models.CharField(max_length=255)
    goal = models.CharField(
        max_length=20,
        choices=[('DAILY', 'Daily'), ('NO_GOAL', 'No Goal')],
        default='DAILY'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.habit1} & {self.habit2}'