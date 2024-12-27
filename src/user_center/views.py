

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View

import exercise_info
import health_profile
import pytz
from datetime import datetime

def get_user_info(request):
    if request.user.is_authenticated:
        # 获取当前登录用户
        current_user = request.user
        # 获取用户名
        username = current_user.username
        # 获取用户ID（Django中通常使用pk作为主键）
        user_id = current_user.id
        # 获取用户注册日期
        join_date = current_user.date_joined

        # 将信息打包成字典
        user_info = {
            'username': username,
            'user_id': user_id,
            'join_date': join_date
        }

        # 获取运动记录数
        exercises = exercise_info.models.ExerciseRecord.objects.filter(user_id=current_user.id).order_by('exercise_id')
        exercises_count = exercises.count()

        # 获取目标完成数
        goals = exercise_info.models.ExerciseGoal.objects.filter(user_id=current_user.id).order_by('exercise_goal_id')
        complete_cnt = 0
        for goal in goals:
            records = exercise_info.models.ExerciseRecord.objects.filter(start_time__gte=goal.start_time, end_time__lte=goal.end_time)
            total_calories = sum(record.calorie_cost for record in records)
            progress = (total_calories / goal.target_calorie_cost) * 100 if goal.target_calorie_cost else 0
            timenow = timezone.now().astimezone(pytz.timezone('Asia/Shanghai'))
            # 将时间格式化为字符串，并替换时区部分
            now_str = timenow.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + '+0000'
            # 将字符串解析回datetime对象，注意这里的格式字符串需要与now_str的格式匹配
            now_datetime = datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S.%f%z')

            if progress >= 100:
                complete_cnt = complete_cnt + 1

        # 获取运动记录数
        health_profiles = health_profile.models.HealthProfile.objects.filter(user=request.user).order_by('-timestamp')
        health_profile_count = health_profiles.count()
        return render(request, 'user_center/user_center.html', {'user_info': user_info, 'exercises_count': exercises_count, 'complete_count': complete_cnt, 'health_profile_count': health_profile_count})
    else:
        # 如果用户未登录，返回一个错误信息或者重定向到登录页面
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')


from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('newPassword')

        request.user.set_password(new_password)
        request.user.save()

    return render(request, 'user_center/reset_password.html')


@login_required
def validate_current_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        user = authenticate(username=request.user.username, password=current_password)

        if user is not None:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})


@login_required
def edit_username(request):
    if request.user.is_authenticated:
        # 获取当前登录用户
        current_user = request.user
        # 获取用户名
        username = current_user.username
        # 获取用户ID（Django中通常使用pk作为主键）
        user_id = current_user.id
        # 获取用户注册日期
        join_date = current_user.date_joined

        # 将信息打包成字典
        user_info = {
            'username': username,
            'user_id': user_id,
            'join_date': join_date
        }

        # 获取运动记录数
        exercises = exercise_info.models.ExerciseRecord.objects.filter(user_id=current_user.id).order_by('exercise_id')
        exercises_count = exercises.count()

        # 获取目标完成数
        goals = exercise_info.models.ExerciseGoal.objects.filter(user_id=current_user.id).order_by('exercise_goal_id')
        complete_cnt = 0
        for goal in goals:
            records = exercise_info.models.ExerciseRecord.objects.filter(start_time__gte=goal.start_time, end_time__lte=goal.end_time)
            total_calories = sum(record.calorie_cost for record in records)
            progress = (total_calories / goal.target_calorie_cost) * 100 if goal.target_calorie_cost else 0
            timenow = timezone.now().astimezone(pytz.timezone('Asia/Shanghai'))
            # 将时间格式化为字符串，并替换时区部分
            now_str = timenow.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + '+0000'
            # 将字符串解析回datetime对象，注意这里的格式字符串需要与now_str的格式匹配
            now_datetime = datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S.%f%z')

            if progress >= 100:
                complete_cnt = complete_cnt + 1

        # 获取运动记录数
        health_profiles = health_profile.models.HealthProfile.objects.filter(user=request.user).order_by('-timestamp')
        health_profile_count = health_profiles.count()

        # 处理用户名修改
        if request.method == 'POST':
            new_username = request.POST.get('change_user_name')
            if not new_username:
                messages.error(request, "用户名不能为空！")
            elif User.objects.filter(username=new_username).exists():
                messages.error(request, "该用户名已被使用，请选择其他用户名。")
            else:
                current_user.username = new_username
                current_user.save()
                messages.success(request, "用户名修改成功！")
                return redirect('edit_username')  # 或重定向到其他页面

        # 渲染模板
        return render(request, 'user_center/edit_username.html', {
            'user_info': user_info,
            'exercises_count': exercises_count,
            'complete_count': complete_cnt,
            'health_profile_count': health_profile_count,
        })

    else:
        # 如果用户未登录，返回一个错误信息或者重定向到登录页面
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')