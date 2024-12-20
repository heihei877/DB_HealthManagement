from django.urls import path
from . import views

urlpatterns = [
    path('exercise_record/', views.exercise_record_list, name="exercise_record_list"),
    path('exercise_record/<int:exerciseid>/', views.exercise_record_detail, name="exercise_record_detail"),
    path('add_exercise_record/', views.add_exercise_record, name="add_exercise_record"),
    path('delete_exercise_record/<int:exerciseid>/', views.delete_exercise_record, name='delete_exercise_record'),
]