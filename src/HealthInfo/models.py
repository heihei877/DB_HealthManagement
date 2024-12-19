from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ExerciseRecord(models.Model):
    ExerciseId = models.AutoField(primary_key=True)
    UserId = models.IntegerField()
    Type = models.CharField(max_length=30)
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()
    CalorieCost = models.IntegerField()

