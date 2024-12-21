from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_profile_list.as_view(), name='health_profile_list'),
    path('add/', views.add_health_profile.as_view(), name='add_health_profile'),
    path('delete/<int:health_profile_id>/', views.delete_health_profile.as_view(), name='delete_health_profile'),
    path('analysis/', views.health_profile_analysis.as_view(), name='health_profile_analysis'),
]