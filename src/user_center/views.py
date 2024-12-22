from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse


from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View

def get_user_info(request):
    if request.user.is_authenticated:
        # 获取当前登录用户
        current_user = request.user
        # 获取用户名
        username = current_user.username
        # 获取用户ID（Django中通常使用pk作为主键）
        user_id = current_user.pk
        # 获取用户注册日期
        join_date = current_user.date_joined

        # 将信息打包成字典
        user_info = {
            'username': username,
            'user_id': user_id,
            'join_date': join_date
        }

        return render(request, 'user_center/user_center.html', {'user_info': user_info})
    else:
        # 如果用户未登录，返回一个错误信息或者重定向到登录页面
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')


