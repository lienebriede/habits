from django.urls import path
from .views import UserProfileView, ProfileVisibilityView, FollowUnfollowView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('<str:username>/', ProfileVisibilityView.as_view(), name='profile-visibility'),
    path('follow/<str:username>/', FollowUnfollowView.as_view(), name='follow-unfollow'),
]