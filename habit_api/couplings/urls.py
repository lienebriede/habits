from django.urls import path
from . import views

urlpatterns = [
    path('couplings/', views.CouplingList.as_view(), name='coupling-list'),
    path('couplings/<int:pk>/', views.CouplingDetail.as_view(), name='coupling-detail'),
]