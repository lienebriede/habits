from django.apps import AppConfig


class HabitStackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habit_stacking'

    # Signal handlers
    def ready(self):
            import habit_stacking.signals