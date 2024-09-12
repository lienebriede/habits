from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.ProfileDetail.as_view(), name='profile-detail'),
]