from django.db import models
from django.contrib.auth.models import User
from couplings.models import Coupling

class DayOfWeek(models.Model):
    day_name = models.CharField(max_length=10)

    def __str__(self):
        return self.day_name

class HabitTracking(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('SPECIFIC_DAYS', 'Specific Days'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupling = models.ForeignKey(Coupling, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False)
    goal = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='DAILY')
    specific_days = models.ManyToManyField(DayOfWeek, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.coupling} on {self.date}'