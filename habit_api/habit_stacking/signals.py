from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HabitStacking, HabitStackingLog
from datetime import timedelta
from django.utils import timezone

@receiver(post_save, sender=HabitStacking)
def create_or_update_logs(sender, instance, **kwargs):
    today = timezone.now().date()
    one_year_ago = today - timedelta(days=365)

    if instance.goal == 'DAILY':
        date = one_year_ago
        while date <= today:
            log, created = HabitStackingLog.objects.get_or_create(
                habit_stack=instance,
                user=instance.user,
                date=date,
                defaults={'completed': False}
            )
            date += timedelta(days=1)