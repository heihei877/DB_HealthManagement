from django.contrib import messages

from exercise_info import models

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render, redirect
from .models import ExerciseRecord, ExerciseGoal
from .forms import ExerciseRecordForm, ExerciseGoalForm


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

# 返回所有运动目标
def exercise_goal_list(request):
    # goals = ExerciseGoal.objects.all()
    # return render(request, 'exercise_info/exercise_goal_list.html', {'goals': goals})
    goals = ExerciseGoal.objects.all()
    goals_with_progress = []
    for goal in goals:
        records = ExerciseRecord.objects.filter(start_time__gte=goal.start_time, end_time__lte=goal.end_time)
        total_calories = sum(record.calorie_cost for record in records)
        progress = (total_calories / goal.target_calorie_cost) * 100 if goal.target_calorie_cost else 0
        goals_with_progress.append({
            'goal': goal,
            'progress': progress,
            'is_completed': progress >= 100
        })
    return render(request, 'exercise_info/exercise_goal_list.html', {'goals': goals_with_progress})

# 增加运动目标
def add_exercise_goal(request):
    current_user = request.user
    if request.method == 'POST':
        form = ExerciseGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user_id = current_user.id
            goal.save()
            return redirect('exercise_goal_list')
        else:
            print(form.errors)
            messages.error(request, "无效的运动目标！")
    else:
        form = ExerciseGoalForm()
    return render(request, 'exercise_info/add_exercise_goal.html', {'form': form})

# 修改运动目标
def exercise_goal_update(request, exerciseGoal_id):
    goal = get_object_or_404(ExerciseGoal, exerciseGoal_id=exerciseGoal_id)
    current_user = request.user
    if request.method == 'POST':
        form = ExerciseGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            ExerciseGoal.user_id = current_user.id
            return redirect('exercise_info/exercise_goal_list')
    else:
        form = ExerciseGoalForm(instance=goal)
    return render(request, 'exercise_info/exercise_goal_list.html', {'form': form})

# 删除运动目标
def exercise_goal_delete(request, exerciseGoal_id):
    goal = get_object_or_404(ExerciseGoal, exerciseGoal_id=exerciseGoal_id)
    # current_user = request.user
    if request.method == 'POST':
        goal.delete()
        return redirect('exercise_goal_list')
    return render(request, 'exercise_info/exercise_goal_list.html', {'goal': goal})