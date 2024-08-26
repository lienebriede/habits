from django.contrib import admin
from .models import HabitStacking

@admin.register(HabitStacking)
class HabitStackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit1', 'habit2', 'goal', 'created_at')
    list_filter = ('goal',)
    search_fields = ('user__username', 'habit1', 'habit2')
