from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from .models import Profile, Follow
from .serializers import ProfileSerializer, FollowSerializer
from habit_api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

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

class ProfileVisibilityView(generics.RetrieveAPIView):
    """
    Retrieve the profile of another user. Only accessible if the requester follows the user
    or if the profile is public.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Retrieve the profile object for the specified username.
        """
        username = self.kwargs.get('username')
        try:
            profile = Profile.objects.get(owner__username=username)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found")

        # Check if the user is allowed to view this profile
        if profile.is_private and not Follow.objects.filter(follower=self.request.user, followed_user=profile.owner).exists():
            raise PermissionDenied("You do not have permission to view this profile")

        return profile

class FollowUnfollowView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, username):
        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if followed_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the follow relationship already exists
        follow_instance, created = Follow.objects.get_or_create(
            follower=request.user, followed_user=followed_user
        )

        if not created:
            # If it already exists, unfollow (delete follow)
            follow_instance.delete()
            return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_200_OK)

        return Response({"detail": "Followed successfully"}, status=status.HTTP_201_CREATED)