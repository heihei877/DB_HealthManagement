from django.contrib import messages

from exercise_info import models

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render, redirect
from .models import ExerciseRecord
from .forms import ExerciseRecordForm


# Create your views here.

# 返回所有的运动记录
def exercise_record_list(request):
    exercises = models.ExerciseRecord.objects.all().order_by('exercise_id')
    exercises_with_duration = []
    for exercise in exercises:
        duration = exercise.end_time - exercise.start_time
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        exercises_with_duration.append({
            'exercise': exercise,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        })
    return render(request, "exercise_info/exercise_record_list.html", {"exercises": exercises_with_duration})
    # return render(request, "exercise_info/exercise_record_list.html", {"exercises": exercises})


# 返回指定id的运动记录
def exercise_record_detail(request, exerciseid):
    if exerciseid > 0:
        exercise = get_object_or_404(ExerciseRecord, exercise_id=exerciseid)
        return render(request, 'exercise_info/exercise_record_detail.html', {'exercise': exercise})
    else:
        exerciseid = request.GET.get('exerciseid', None)
        if exerciseid:
            try:
                exercise = ExerciseRecord.objects.get(exercise_id=exerciseid)
                return render(request, 'exercise_info/exercise_record_detail.html', {'exercise': exercise})
            except ExerciseRecord.DoesNotExist:
                raise Http404("运动记录未找到。")
        return render(request, 'exercise_info/exercise_record_list.html')


# 增加运动记录
def add_exercise_record(request):
    current_user = request.user

    if request.method == 'POST':
        form = ExerciseRecordForm(request.POST)

        if form.is_valid():
            exercise_record = form.save(commit=False)
            exercise_record.user_id = current_user.id  # 填充 user_id
            exercise_record.save()  # 保存数据
            return redirect('exercise_record_list')
        else:
            print(form.errors)
            messages.error(request, "无效的运动记录！")
    else:
        form = ExerciseRecordForm()

    return render(request, 'exercise_info/add_exercise_record.html', {'form': form})


# 删除运动记录
def delete_exercise_record(request, exerciseid):
    exercise = get_object_or_404(ExerciseRecord, exercise_id=exerciseid)
    exercise.delete()
    return redirect('exercise_record_list')

