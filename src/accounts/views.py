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

class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "您已登录，无法再次注册！")
            return redirect('index')
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        check_password = request.POST.get('check_password', '')

        # Check for empty values
        if not username or not password or not check_password:
            return JsonResponse({'success': False, 'error': '用户名和密码不能为空！'})

        # Check password consistency
        if password != check_password:
            return JsonResponse({'success': False, 'error': '密码与确认密码不一致！'})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': '该账号已注册！'})

        # Create the new user
        User.objects.create_user(username=username, password=password)
        return JsonResponse({'success': True})



class Login(View):
    def get(self, request):
        # 已登录用户不允许再次登录
        if request.user.is_authenticated:
            messages.info(request, "您已登录，无法再次登录！")  # 增加提示信息
            return redirect('index')  # 跳转到首页
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 检查空值
        if not username or not password:
            messages.error(request, "用户名和密码不能为空！")
            return redirect(reverse('login'))  # 重新定向到登录页，显示错误信息

        # 验证用户是否存在
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # 用户验证成功后，进行登录
            return redirect('index')  # 登录成功，跳转到首页
        else:
            messages.error(request, "用户名或密码错误！")  # 用户名或密码错误
            return redirect(reverse('login'))  # 登录失败，返回登录页


def user_logout(request):
    logout(request)  # 执行注销操作
    return render(request, 'accounts/logout.html')