from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Habit
from .serializers import HabitSerializer
from habit_api.permissions import IsOwnerOrReadOnly

class HabitList(APIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        habits = Habit.objects.all()
        serializer = HabitSerializer(
            habits, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = HabitSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

class HabitDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = HabitSerializer

    def get_object(self, pk):
        try:
            habit = Habit.objects.get(pk=pk)
            self.check_object_permissions(self.request, habit)
            return habit
        except Habit.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        habit = self.get_object(pk)
        serializer = HabitSerializer(
            habit, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        habit = self.get_object(pk)
        serializer = HabitSerializer(
            habit, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        habit = self.get_object(pk)
        habit.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )