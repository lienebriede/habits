from django.db import models
from django.contrib.auth.models import User

class Coupling(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    habit1 = models.ForeignKey('habits.Habit', related_name='habit1', on_delete=models.CASCADE)
    habit2 = models.ForeignKey('habits.Habit', related_name='habit2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('habit1', 'habit2', 'owner')

    def __str__(self):
        return f'{self.habit1.name} + {self.habit2.name}'