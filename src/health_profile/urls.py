from django.urls import path
from . import views

urlpatterns = [
    # path('', views.health_profile_list, name='health_profile_list'),
    path('add/', views.add_health_profile.as_view(), name='add_health_profile'),
    # path('delete/<int:profile_id>/', views.delete_health_profile, name='delete_health_profile'),
]