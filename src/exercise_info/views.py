from django.contrib import messages
from datetime import datetime
from django.utils import timezone

from exercise_info import models

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render, redirect
from .models import ExerciseRecord, ExerciseGoal
from .forms import ExerciseRecordForm, ExerciseGoalForm

import pytz


# Create your views here.

# 返回所有的运动记录
def exercise_record_list(request):
    # exercises = models.ExerciseRecord.objects.all().order_by('exercise_id')
    current_user = request.user
    exercises = models.ExerciseRecord.objects.filter(user_id=current_user.id).order_by('exercise_id')
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
    print("deleting!")
    exercise = get_object_or_404(ExerciseRecord, exercise_id=exerciseid)
    exercise.delete()
    return redirect('exercise_record_list')


# 返回所有运动目标
def exercise_goal_list(request):
    current_user = request.user
    # goals = ExerciseGoal.objects.all()
    # return render(request, 'exercise_info/exercise_goal_list.html', {'goals': goals})
    goals = ExerciseGoal.objects.filter(user_id=current_user.id).order_by('exercise_goal_id')
    goals_with_progress = []
    total_cnt = 0
    complete_cnt = 0
    uncompleted_cnt = 0
    for goal in goals:
        total_cnt = total_cnt + 1
        records = ExerciseRecord.objects.filter(start_time__gte=goal.start_time, end_time__lte=goal.end_time)
        total_calories = sum(record.calorie_cost for record in records)
        progress = (total_calories / goal.target_calorie_cost) * 100 if goal.target_calorie_cost else 0
        timenow = timezone.now().astimezone(pytz.timezone('Asia/Shanghai'))
        # 将时间格式化为字符串，并替换时区部分
        now_str = timenow.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + '+0000'
        # 将字符串解析回datetime对象，注意这里的格式字符串需要与now_str的格式匹配
        now_datetime = datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S.%f%z')

        if progress >= 100:
            complete_cnt = complete_cnt + 1

        else:
            if now_datetime > goal.end_time:  # 截止
                timeout = 1
                uncompleted_cnt = uncompleted_cnt + 1
            else:
                timeout = 0

        goals_with_progress.append({
            'goal': goal,
            'progress': progress,
            'is_completed': progress >= 100,
            'timeout': timeout
        })
    doing_cnt = total_cnt - uncompleted_cnt - complete_cnt;
    return render(request, 'exercise_info/exercise_goal_list.html',
                  {'goals': goals_with_progress, 'total_count': total_cnt, 'complete_count': complete_cnt,
                   'uncomplete_count': uncompleted_cnt, 'doing_count': doing_cnt})


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
    goal = get_object_or_404(ExerciseGoal, exercise_goal_id=exerciseGoal_id)
    # current_user = request.user
    if request.method == 'POST':
        goal.delete()
        return redirect('exercise_goal_list')
    return render(request, 'exercise_info/exercise_goal_list.html', {'goal': goal})
