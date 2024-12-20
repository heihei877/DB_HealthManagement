from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HealthProfileForm, UserCustomFieldForm
from .models import HealthProfile, UserCustomField


@login_required
def create_health_profile(request):
    if request.method == 'POST':
        health_form = HealthProfileForm(request.POST)
        custom_form = UserCustomFieldForm(request.POST)

        if health_form.is_valid() and custom_form.is_valid():
            # 创建健康记录
            health_profile = health_form.save(commit=False)
            health_profile.user = request.user  # 关联到当前登录的用户
            health_profile.save()

            # 创建自定义字段
            custom_field = custom_form.save(commit=False)
            custom_field.health_profile = health_profile  # 关联到刚创建的健康记录
            custom_field.save()

            return redirect('health_profile_list')  # 重定向到健康记录列表页面
    else:
        health_form = HealthProfileForm()
        custom_form = UserCustomFieldForm()

    return render(request, 'health_profile/add_health_profile.html', {
        'health_form': health_form,
        'custom_form': custom_form
    })
