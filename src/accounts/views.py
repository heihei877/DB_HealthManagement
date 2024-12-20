from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse


class Register(View):
    def get(self, request):
        # 已登录用户不允许再次注册
        if request.user.is_authenticated:
            messages.info(request, "您已登录，无法再次注册！")  # 增加提示信息
            return redirect(reverse('index'))  # 跳转到首页
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        check_password = request.POST.get('check_password', '')

        # 检查空值
        if not username or not password or not check_password:
            messages.error(request, "用户名和密码不能为空！")
            return redirect(reverse('register'))

        # 检查密码一致性
        if password != check_password:
            messages.error(request, "密码与确认密码不一致！")
            return redirect(reverse('register'))

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, "该账号已注册！")
            return redirect(reverse('register'))

        # 创建新用户
        User.objects.create_user(username=username, password=password)
        messages.success(request, "注册成功，请登录！")
        return redirect(reverse('login'))


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