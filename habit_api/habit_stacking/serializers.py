from rest_framework import serializers
from .models import HabitStacking

class HabitStackingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = HabitStacking
        fields = ['id', 'user', 'habit1', 'habit2', 'goal', 'created_at']