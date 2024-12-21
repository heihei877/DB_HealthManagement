from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from .models import HealthProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class add_health_profile(View):
    def get(self, request):
        return render(request, 'health_profile/add_health_profile.html')

    def post(self, request):
        # 获取POST数据
        height = request.POST.get('height', None)
        weight = request.POST.get('weight', None)
        systolic_bp = request.POST.get('systolic_bp', None)
        diastolic_bp = request.POST.get('diastolic_bp', None)
        blood_sugar = request.POST.get('blood_sugar', None)

        # 检查是否有有效的数据
        if not any([height, weight, systolic_bp, diastolic_bp, blood_sugar]):
            messages.error(request, "请至少填写一个字段！")
            return redirect('add_health_profile')

        # 创建健康记录对象并填充字段
        health_profile = HealthProfile(
            user=request.user,
            height=height if height else None,
            weight=weight if weight else None,
            systolic_bp=systolic_bp if systolic_bp else None,
            diastolic_bp=diastolic_bp if diastolic_bp else None,
            blood_sugar=blood_sugar if blood_sugar else None
        )

        try:
            # 保存记录
            health_profile.save()
            messages.success(request, "健康记录已成功添加！")
            # 重定向到健康记录列表页面
            return redirect('health_profile_list')
        except Exception as e:
            messages.error(request, f"添加健康记录失败: {str(e)}")
            return redirect('add_health_profile')
