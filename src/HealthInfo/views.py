from HealthInfo import models

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render, redirect
from .models import ExerciseRecord
from .forms import ExerciseRecordForm


# Create your views here.

# 返回所有的运动记录
def exercise_record_list(request):
    exercises = models.ExerciseRecord.objects.all()
    return render(request, "exercise_record_list.html", {"exercises": exercises})


# 返回指定id的运动记录
def exercise_record_detail(request, exerciseid):
    if exerciseid > 0:
        exercise = get_object_or_404(ExerciseRecord, exercise_id=exerciseid)
        return render(request, 'exercise_record_detail.html', {'exercise': exercise})
    else:
        exerciseid = request.GET.get('exerciseid', None)
        if exerciseid:
            try:
                exercise = ExerciseRecord.objects.get(exercise_id=exerciseid)
                return render(request, 'exercise_record_detail.html', {'exercise': exercise})
            except ExerciseRecord.DoesNotExist:
                raise Http404("运动记录未找到。")
        return render(request, 'exercise_record_list.html')


# 增加运动记录
def add_exercise_record(request):
    if request.method == 'POST':
        form = ExerciseRecordForm(request.POST)
        if form.is_valid():
            form.save()  # 保存数据到数据库
            return redirect('exercise_record_list')  # 保存后跳转到运动记录列表页
    else:
        form = ExerciseRecordForm()  # 初始化一个空表单

    return render(request, 'add_exercise_record.html', {'form': form})


# 删除运动记录
def delete_exercise_record(request, exerciseid):
    exercise = get_object_or_404(ExerciseRecord, exercise_id=exerciseid)
    exercise.delete()
    return redirect('exercise_record_list')

# 返回index.html页面
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')  # 如果用户未登录，跳转到登录页面

    # 获取当前用户的运动记录
    exercises = ExerciseRecord.objects.filter(user_id=request.user.id)
    return render(request, 'index.html', {'exercises': exercises})
