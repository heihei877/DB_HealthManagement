from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_info, name='user_center'),
    path('change_password/', views.change_password, name='change_password'),
    path('validate_current_password/', views.validate_current_password, name='validate_current_password'),
]