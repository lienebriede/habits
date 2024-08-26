from rest_framework import generics, permissions
from .models import HabitStacking, HabitStackingLog
from .serializers import HabitStackingSerializer, HabitStackingLogSerializer

class HabitStackingListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitStackingSerializer

    def get_queryset(self):
        return HabitStacking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitStackingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitStackingSerializer

    def get_queryset(self):
        return HabitStacking.objects.filter(user=self.request.user)

class HabitStackingLogListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitStackingLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitStackingLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit_stack = serializer.validated_data['habit_stack']
        if habit_stack.user != self.request.user:
            raise serializers.ValidationError("You cannot log habits that don't belong to you.")
        serializer.save(user=self.request.user)