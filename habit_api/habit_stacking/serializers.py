from rest_framework import serializers
from .models import HabitStacking, HabitStackingLog

class HabitStackingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = HabitStacking
        fields = ['id', 'user', 'habit1', 'habit2', 'goal', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        habit1 = data.get('habit1')
        habit2 = data.get('habit2')

        if HabitStacking.objects.filter(
            user=user,
            habit1=habit1,
            habit2=habit2,
        ).exists():
            raise serializers.ValidationError("A habit stack with these details already exists.")

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