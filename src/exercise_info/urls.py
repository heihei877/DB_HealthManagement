from django.urls import path
from . import views

urlpatterns = [
    path('exercise_record/', views.exercise_record_list, name="exercise_record_list"),
    path('add_exercise_record/', views.add_exercise_record, name="add_exercise_record"),
    path('delete_exercise_record/<int:exerciseid>/', views.delete_exercise_record, name='delete_exercise_record'),
    path('exercise_goal/', views.exercise_goal_list, name = 'exercise_goal_list'),
    path('add_exercise_goal/', views.add_exercise_goal, name = 'add_exercise_goal'),
]
