from django.urls import path
from .views import HabitStackingListCreateView, HabitStackingDetailView, HabitStackingLogListCreateView, PredefinedHabitListView

urlpatterns = [
    path('habit-stacking/', HabitStackingListCreateView.as_view(), name='habit-stacking-list-create'),
    path('habit-stacking/<int:pk>/', HabitStackingDetailView.as_view(), name='habit-stacking-detail'),
    path('habit-stacking-logs/', HabitStackingLogListCreateView.as_view(), name='habit-stacking-log-list-create'),
    path('predefined-habits/', PredefinedHabitListView.as_view(), name='predefined-habits-list'),
]