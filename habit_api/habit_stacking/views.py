from rest_framework import generics
from .models import HabitStacking
from .serializers import HabitStackingSerializer

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