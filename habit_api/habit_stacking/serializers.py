from rest_framework import serializers
from .models import HabitStacking, HabitStackingLog, Weekday, PredefinedHabit

# Serializer for HabitStacking model
class HabitStackingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    specific_days = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Weekday.objects.all(),
        required=False
    )
    predefined_habit1 = serializers.PrimaryKeyRelatedField(
        queryset=PredefinedHabit.objects.all(),
        required=False,
        allow_null=True
    )
    predefined_habit2 = serializers.PrimaryKeyRelatedField(
        queryset=PredefinedHabit.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = HabitStacking
        fields = ['id', 'user', 'predefined_habit1', 'custom_habit1', 'predefined_habit2', 'custom_habit2', 'goal', 'specific_days', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        predefined_habit1 = data.get('predefined_habit1')
        custom_habit1 = data.get('custom_habit1')
        predefined_habit2 = data.get('predefined_habit2')
        custom_habit2 = data.get('custom_habit2')
        goal = data.get('goal')
        specific_days = data.get('specific_days', [])

        # Validation for habit1 and habit2
        if predefined_habit1 and custom_habit1:
            raise serializers.ValidationError("You can only choose either a predefined habit or a custom habit for Habit 1, not both.")
        if predefined_habit2 and custom_habit2:
            raise serializers.ValidationError("You can only choose either a predefined habit or a custom habit for Habit 2, not both.")
        if not (predefined_habit1 or custom_habit1):
            raise serializers.ValidationError("You must provide either a predefined habit or a custom habit for Habit 1.")
        if not (predefined_habit2 or custom_habit2):
            raise serializers.ValidationError("You must provide either a predefined habit or a custom habit for Habit 2.")

        # Ensure habit1 and habit2 are not the same
        if (predefined_habit1 and predefined_habit2 and predefined_habit1 == predefined_habit2) or \
           (custom_habit1 and custom_habit2 and custom_habit1 == custom_habit2) or \
           (predefined_habit1 and custom_habit2 and predefined_habit1.name == custom_habit2) or \
           (predefined_habit2 and custom_habit1 and predefined_habit2.name == custom_habit1):
            raise serializers.ValidationError("Habit1 and Habit2 cannot be the same.")

        # Ensure that either predefined habit or custom habit is provided, but not both empty
        if not ((predefined_habit1 or custom_habit1) and (predefined_habit2 or custom_habit2)):
            raise serializers.ValidationError("Both habit fields cannot be empty. Provide either predefined or custom habits.")


        # Ensure no duplicate habit stacks for the same user
        if HabitStacking.objects.filter(
            user=user,
            predefined_habit1=predefined_habit1,
            custom_habit1=custom_habit1,
            predefined_habit2=predefined_habit2,
            custom_habit2=custom_habit2,
        ).exists():
            raise serializers.ValidationError("A habit stack with these details already exists.")

        # Validate goal value
        if goal not in ['DAILY', 'NO_GOAL', 'SPECIFIC_DAYS']:
            raise serializers.ValidationError("Invalid goal value.")

        # Specific validation rules based on goal
        if goal == 'SPECIFIC_DAYS':
            if not specific_days:
                raise serializers.ValidationError("Specific days must be provided when the goal is 'SPECIFIC_DAYS'.")
        elif goal in ['DAILY', 'NO_GOAL']:
            if specific_days:
                raise serializers.ValidationError("Specific days should not be provided when the goal is 'DAILY' or 'NO_GOAL'.")

        return data

# Serializer for HabitStackingLog model
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

# Serializer for PredefinedHabit model
class PredefinedHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedHabit
        fields = ['id', 'name']