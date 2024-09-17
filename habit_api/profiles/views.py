from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from habit_api.permissions import IsOwnerOrReadOnly

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Return the profile for the currently authenticated user.
        """
        user = self.request.user
        return Profile.objects.filter(owner=user)

    def get_object(self):
        """
        Retrieve the profile object for the currently authenticated user.
        """
        queryset = self.get_queryset()
        try:
            return queryset.get()
        except Profile.DoesNotExist:
            raise NotFound("Profile not found")

    def update(self, request, *args, **kwargs):
        """
        Handle PUT and PATCH requests to update the profile.
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete the profile.
        """
        profile = self.get_object()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)