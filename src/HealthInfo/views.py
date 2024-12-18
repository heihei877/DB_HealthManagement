from django.shortcuts import render
from HealthInfo import models
# Create your views here.
def exercise_record_view(request):
    exercise_queryset = models.ExerciseRecord.objects.all()
    return render(request, "exercise_record.html", {"exercise_queryset": exercise_queryset})
