from rest_framework import serializers
from .models import Habit

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Habit
        fields = [
            'id', 'owner', 'name', 'description', 'frequency'
        ]