from rest_framework import generics, permissions
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

        # Save the habit log and create or update milestone
        habit_log = serializer.save(user=self.request.user)

        print(f"Log created: {habit_log}")

        if habit_log.completed:
            print("Calling create_or_update_milestone")
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