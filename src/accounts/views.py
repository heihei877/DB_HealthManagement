from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse


class Register(View):

    def get(self, request):
        # 已登录用户不允许再次注册
        if request.user.is_authenticated:
            return redirect(reverse('index'))
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
            return redirect(reverse('index'))
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 检查空值
        if not username or not password:
            messages.error(request, "用户名和密码不能为空！")
            return redirect(reverse('login'))

        # 验证用户是否存在
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request, "用户名或密码错误！")
            return redirect(reverse('login'))
