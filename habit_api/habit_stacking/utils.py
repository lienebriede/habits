from django.utils import timezone
from .models import Milestone, HabitStackingLog
import logging

logger = logging.getLogger(__name__)

def create_or_update_milestone(user, habit_stack):
    logger.info("create_or_update_milestone called")
    print("create_or_update_milestone called") 
    
    # Count the number of completed habit stacking logs for the user and the habit stack
    completed_logs = HabitStackingLog.objects.filter(
        habit_stack=habit_stack,
        user=user,
        completed=True
    ).count()

    logger.info(f"Completed logs: {completed_logs} for habit stack: {habit_stack}")

    # Check if it's a milestone-worthy completion (e.g., every 10 completions)
    if completed_logs > 0 and completed_logs % 10 == 0:
        milestone, created = Milestone.objects.get_or_create(
            user=user,
            habit_stack=habit_stack,
            days_completed=completed_logs
        )
        if created:
            milestone.date_achieved = timezone.now().date()
            milestone.save()
            logger.info(f"Milestone created: {milestone}")
        else:
            logger.info(f"Milestone already exists: {milestone}")
    else:
        logger.info(f"No milestone reached yet for {user.username} on {habit_stack}.")
