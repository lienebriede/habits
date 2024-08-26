from django.urls import path
from .views import HabitStackingListCreateView, HabitStackingDetailView

urlpatterns = [
    path('habit-stacking/', HabitStackingListCreateView.as_view(), name='habit-stacking-list-create'),
    path('habit-stacking/<int:pk>/', HabitStackingDetailView.as_view(), name='habit-stacking-detail'),
]