from django.urls import path
from .views import (
    UserProfileView, ProfileVisibilityView, FollowUnfollowView, 
    FollowersListView, FollowingListView, FeedView
)

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<str:username>/', ProfileVisibilityView.as_view(), name='profile-visibility'),
    path('follow/<str:username>/', FollowUnfollowView.as_view(), name='follow-unfollow'),
    path('me/followers/', FollowersListView.as_view(), name='followers-list'),
    path('me/following/', FollowingListView.as_view(), name='following-list'),
]