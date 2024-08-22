from rest_framework import generics, permissions
from .models import Coupling
from .serializers import CouplingSerializer
from habit_api.permissions import IsOwnerOrReadOnly

class CouplingList(generics.ListCreateAPIView):
    """
    List all couplings for the authenticated user or create a new coupling.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CouplingSerializer

    def get_queryset(self):
        """
        Return the list of couplings that belong to the currently authenticated user.
        """
        return Coupling.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Set the owner of the coupling to the currently authenticated user before saving.
        """
        serializer.save(owner=self.request.user)


class CouplingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific coupling for the authenticated user.
    """
    serializer_class = CouplingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Return the coupling object that belongs to the currently authenticated user.
        """
        return Coupling.objects.filter(owner=self.request.user)
