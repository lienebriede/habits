from django.contrib import admin
from .models import HabitStacking, HabitStackingLog, PredefinedHabit, Milestone

class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit_stack', 'days_completed', 'date_achieved')
    search_fields = ('user__username', 'habit_stack__custom_habit1', 'habit_stack__custom_habit2')
    list_filter = ('user', 'date_achieved')

class PredefinedHabitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HabitStackingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'get_habit1', 
        'get_habit2', 
        'goal', 
        'created_at'
    )
    list_filter = ('goal', 'created_at')
    search_fields = ('user__username', 'predefined_habit1__name', 'custom_habit1', 'predefined_habit2__name', 'custom_habit2')
    readonly_fields = ('created_at',)

    def get_habit1(self, obj):
        if obj.predefined_habit1:
            return obj.predefined_habit1.name
        return obj.custom_habit1
    get_habit1.short_description = 'Habit 1'

    def get_habit2(self, obj):
        if obj.predefined_habit2:
            return obj.predefined_habit2.name
        return obj.custom_habit2
    get_habit2.short_description = 'Habit 2'

class HabitStackingLogAdmin(admin.ModelAdmin):
    list_display = ('habit_stack', 'user', 'date', 'completed')
    list_filter = ('completed', 'date')
    search_fields = ('habit_stack__user__username', 'date')

admin.site.register(PredefinedHabit, PredefinedHabitAdmin)
admin.site.register(HabitStacking, HabitStackingAdmin)
admin.site.register(HabitStackingLog, HabitStackingLogAdmin)
admin.site.register(Milestone, MilestoneAdmin)