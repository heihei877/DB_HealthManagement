from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ExerciseRecord(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    type = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calorie_cost = models.IntegerField()

class ExerciseGoal(models.Model):
    exercise_goal_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    type = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    target_calorie_cost = models.IntegerField()



