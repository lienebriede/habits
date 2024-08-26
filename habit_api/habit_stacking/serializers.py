from rest_framework import serializers
from .models import HabitStacking, HabitStackingLog

class HabitStackingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = HabitStacking
        fields = ['id', 'user', 'habit1', 'habit2', 'goal', 'created_at']


class HabitStackingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitStackingLog
        fields = ['habit_stack', 'user', 'date', 'completed']