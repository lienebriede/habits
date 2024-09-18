from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HabitStacking, HabitStackingLog
from datetime import timedelta
from django.utils import timezone

@receiver(post_save, sender=HabitStacking)
def handle_habit_stack_goal_change(sender, instance, **kwargs):
    today = timezone.now().date()
    future_start_date = today

    # Handle goal change from NO_GOAL to DAILY
    if instance.goal == 'DAILY':
        # Create logs from today onwards if goal was previously NO_GOAL
        existing_logs = HabitStackingLog.objects.filter(
            habit_stack=instance,
            user=instance.user,
            date__gte=future_start_date
        )
        
        if not existing_logs.exists():
            # Create logs from today onwards
            date = future_start_date
            while date <= future_start_date + timedelta(days=365):  # Adjust the range as needed
                log, created = HabitStackingLog.objects.get_or_create(
                    habit_stack=instance,
                    user=instance.user,
                    date=date,
                    defaults={'completed': False}
                )
                date += timedelta(days=1)

    # Handle goal change from DAILY to NO_GOAL
    elif instance.goal == 'NO_GOAL':
        # Remove future logs if goal was previously DAILY
        HabitStackingLog.objects.filter(
            habit_stack=instance,
            user=instance.user,
            date__gte=future_start_date
        ).delete()