from rest_framework import generics, permissions
from .models import HabitStacking, HabitStackingLog, PredefinedHabit
from .serializers import HabitStackingSerializer, HabitStackingLogSerializer, PredefinedHabitSerializer
from rest_framework.exceptions import PermissionDenied

# HabitStacking list and create view
class HabitStackingListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitStackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStacking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# HabitStacking retrieve, update, and delete view
class HabitStackingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitStackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStacking.objects.filter(user=self.request.user)

# HabitStackingLog list and create view
class HabitStackingLogListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitStackingLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStackingLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit_stack = serializer.validated_data['habit_stack']
        if habit_stack.user != self.request.user:
            raise PermissionDenied("You cannot log habits that don't belong to you.")
        serializer.save(user=self.request.user)

# PredefinedHabit list view
class PredefinedHabitListView(generics.ListAPIView):
    queryset = PredefinedHabit.objects.all()
    serializer_class = PredefinedHabitSerializer
    permission_classes = [permissions.IsAuthenticated]