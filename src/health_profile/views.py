from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import HealthProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json


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


@method_decorator(login_required, name='dispatch')
class health_profile_list(View):
    def get(self, request):
        # 获取当前用户的健康档案
        health_profiles = HealthProfile.objects.filter(user=request.user).order_by('-timestamp')

        # 提取体重、身高、血糖、血压（高压与低压）数据
        weight_data = [{'date': profile.timestamp.strftime('%Y-%m-%d %H:%M'), 'weight': float(profile.weight)}
                       for profile in health_profiles if profile.weight is not None]

        height_data = [{'date': profile.timestamp.strftime('%Y-%m-%d %H:%M'), 'height': float(profile.height)}
                       for profile in health_profiles if profile.height is not None]

        blood_sugar_data = [
            {'date': profile.timestamp.strftime('%Y-%m-%d %H:%M'), 'blood_sugar': float(profile.blood_sugar)}
            for profile in health_profiles if profile.blood_sugar is not None]

        systolic_bp_data = [
            {'date': profile.timestamp.strftime('%Y-%m-%d %H:%M'), 'systolic_bp': float(profile.systolic_bp)}
            for profile in health_profiles if profile.systolic_bp is not None]

        diastolic_bp_data = [
            {'date': profile.timestamp.strftime('%Y-%m-%d %H:%M'), 'diastolic_bp': float(profile.diastolic_bp)}
            for profile in health_profiles if profile.diastolic_bp is not None]

        systolic_diastolic_bp_data = [
            {
                'date': profile.timestamp.strftime('%Y-%m-%d %H:%M'),
                'systolic_bp': float(profile.systolic_bp),
                'diastolic_bp': float(profile.diastolic_bp)
            }
            for profile in health_profiles if profile.systolic_bp is not None and profile.diastolic_bp is not None
        ]

        # 将数据传递到模板
        return render(request, 'health_profile/health_profile_list.html', {
            'health_profiles': health_profiles,
            'weight_data': json.dumps(weight_data),
            'height_data': json.dumps(height_data),
            'blood_sugar_data': json.dumps(blood_sugar_data),
            'systolic_diastolic_bp_data': json.dumps(systolic_diastolic_bp_data),
        })
