from rest_framework import serializers
from .models import HabitStacking, HabitStackingLog, Weekday

class HabitStackingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    specific_days = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Weekday.objects.all(),
        required=False
    )

    class Meta:
        model = HabitStacking
        fields = ['id', 'user', 'habit1', 'habit2', 'goal', 'specific_days', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        habit1 = data.get('habit1')
        habit2 = data.get('habit2')
        goal = data.get('goal')
        specific_days = data.get('specific_days', [])

        if habit1 == habit2:
            raise serializers.ValidationError("Habit1 and Habit2 cannot be the same.")

        if HabitStacking.objects.filter(
            user=user,
            habit1=habit1,
            habit2=habit2,
        ).exists():
            raise serializers.ValidationError("A habit stack with these details already exists.")

        # Ensure specific_days are provided when goal is 'SPECIFIC_DAYS'
        if goal == 'SPECIFIC_DAYS' and not specific_days:
            raise serializers.ValidationError("Specific days must be provided when the goal is 'Specific Days'.")

        # Ensure no specific_days are provided when goal is 'DAILY' or 'NO_GOAL'
        if goal in ['DAILY', 'NO_GOAL'] and specific_days:
            raise serializers.ValidationError("Specific days should not be provided when the goal is 'Daily' or 'No Goal'.")

        return data


class HabitStackingLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = HabitStackingLog
        fields = ['habit_stack', 'user', 'date', 'completed']

    def validate(self, data):
        habit_stack = data.get('habit_stack')
        user = self.context['request'].user

        if habit_stack.user != user:
            raise serializers.ValidationError("You cannot log habits that don't belong to you.")

        if HabitStackingLog.objects.filter(
            habit_stack=habit_stack,
            user=user,
            date=data.get('date')
        ).exists():
            raise serializers.ValidationError("Log entry already exists for this habit stack on this date.")
            
        return data