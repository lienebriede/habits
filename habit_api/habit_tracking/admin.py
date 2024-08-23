from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import HabitTracking, DayOfWeek

@admin.register(HabitTracking)
class HabitTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupling', 'date', 'status', 'goal')
    list_filter = ('user', 'goal', 'date')
    search_fields = ('user__username', 'coupling__habit1__name', 'coupling__habit2__name')
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('Specific Days', is_stacked=False)},
    }

@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('day_name',)
    search_fields = ('day_name',)