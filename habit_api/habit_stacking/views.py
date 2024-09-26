from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import HabitStacking, HabitStackingLog, PredefinedHabit, Milestone
from .serializers import HabitStackingSerializer, HabitStackingLogSerializer, PredefinedHabitSerializer, MilestoneSerializer
from rest_framework.exceptions import PermissionDenied
from .utils import create_or_update_milestone

# HabitStacking list and create view
class HabitStackingListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitStackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStacking.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# HabitStacking retrieve, update, and delete view
class HabitStackingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitStackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStacking.objects.filter(user=self.request.user).order_by('id')

    def get(self, request, *args, **kwargs):
        habit_stack = self.get_object()
        milestones = Milestone.objects.filter(habit_stack=habit_stack).order_by('-date_achieved')
        
        habit_stack_data = HabitStackingSerializer(habit_stack).data
        milestones_data = MilestoneSerializer(milestones, many=True).data

        return Response({
            'habit_stack': habit_stack_data,
            'milestones': milestones_data,
        })

# HabitStackingLog list and create view
class HabitStackingLogListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitStackingLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStackingLog.objects.filter(user=self.request.user).order_by('date')

    def perform_create(self, serializer):
        habit_stack = serializer.validated_data['habit_stack']
        if habit_stack.user != self.request.user:
            raise PermissionDenied("You cannot log habits that don't belong to you.")

        # Check if we are updating an existing log
        if hasattr(serializer, 'instance') and serializer.instance:
            # If we're updating, we can just save the existing instance
            habit_log = serializer.save(user=self.request.user)
            print(f"Log updated: {habit_log}")
        else:
            # If no instance exists, we create a new log
            habit_log = serializer.save(user=self.request.user)
            print(f"Log created: {habit_log}")

        # Check if the habit log is completed
        if habit_log.completed:
            create_or_update_milestone(self.request.user, habit_stack)

# PredefinedHabit list view
class PredefinedHabitListView(generics.ListAPIView):
    queryset = PredefinedHabit.objects.all().order_by('name')
    serializer_class = PredefinedHabitSerializer
    permission_classes = [permissions.IsAuthenticated]


# Milestone list view
class MilestoneListView(generics.ListAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user).order_by('-date_achieved')