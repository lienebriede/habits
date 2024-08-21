from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer

class HabitCreateView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)