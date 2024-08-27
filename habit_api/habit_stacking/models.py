from django.db import models
from django.contrib.auth.models import User

class HabitStacking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit1 = models.CharField(max_length=255)
    habit2 = models.CharField(max_length=255)

    GOAL_CHOICES = [
        ('DAILY', 'Daily'),
        ('NO_GOAL', 'No Goal'),
        ('SPECIFIC_DAYS', 'Specific Days')
    ]
    goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES,
        default='DAILY'
    )
    specific_days = models.ManyToManyField(
        'Weekday',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'habit1', 'habit2') 

    def __str__(self):
        return f'{self.user.username} - {self.habit1} & {self.habit2}'

        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Weekday(models.Model):
    name = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    
    def __str__(self):
        return self.name


class HabitStackingLog(models.Model):
    habit_stack = models.ForeignKey(HabitStacking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit_stack', 'user', 'date')

    def __str__(self):
        return f'{self.user.username} - {self.habit_stack.habit1} & {self.habit_stack.habit2} - {self.date} - Completed: {self.completed}'