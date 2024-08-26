from rest_framework import serializers
from .models import HabitStacking, HabitStackingLog

class HabitStackingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = HabitStacking
        fields = ['id', 'user', 'habit1', 'habit2', 'goal', 'created_at']


class HabitStackingLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    completed = serializers.BooleanField(default=True)

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

    def create(self, validated_data):
        validated_data.setdefault('completed', True)
        return super().create(validated_data)