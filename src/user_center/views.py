

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

class reset_password(View):
        def get(self, request):
            if not request.user.is_authenticated:
                messages.info(request, "您尚未登录，无法修改密码！")
                return redirect('login')
            form = PasswordChangeForm(request.user)
            return render(request, 'user_center/reset_password.html', {'form': form})

        def post(self, request):
            if not request.user.is_authenticated:
                messages.info(request, "您尚未登录，无法修改密码！")
                return redirect('login')
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # 保持用户登录状态
                messages.success(request, "密码修改成功！")
                return redirect('user_center')
            else:
                for msg in form.error_messages:
                    messages.error(request, form.error_messages[msg][0])
                return render(request, 'user_center/reset_password.html', {'form': form})

UserModel = get_user_model()
class EditUsername(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "您尚未登录，无法修改用户名！")
            return redirect('login')  # 假设有一个名为 'login' 的登录页面
        return render(request, 'user_center/edit_username.html')

    def post(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "您尚未登录，无法修改用户名！")
            return redirect('login')  # 假设有一个名为 'login' 的登录页面

        new_username = request.POST.get('new_username', '')

        # 检查新用户名是否为空
        if not new_username:
            messages.error(request, "用户名不能为空！")
            return render(request, 'user_center/change_username.html')

        # 检查新用户名是否已被占用
        if UserModel.objects.filter(username=new_username).exists():
            messages.error(request, "该用户名已被注册！")
            return render(request, 'user_center/change_username.html')

        # 更新用户名
        request.user.username = new_username
        request.user.save()
        messages.success(request, "用户名修改成功！")
        return redirect('user_center')  # 假设有一个名为 'index' 的主页


