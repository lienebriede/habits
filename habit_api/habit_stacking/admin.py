from django.contrib import admin
from .models import HabitStacking, HabitStackingLog

@admin.register(HabitStacking)
class HabitStackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit1', 'habit2', 'goal', 'created_at')
    list_filter = ('goal',)
    search_fields = ('user__username', 'habit1', 'habit2')


@admin.register(HabitStackingLog)
class HabitStackingLogAdmin(admin.ModelAdmin):
    list_display = ('habit_stack', 'user', 'date', 'completed')
    list_filter = ('date', 'completed', 'habit_stack')
    search_fields = ('habit_stack__habit1', 'habit_stack__habit2', 'user__username')