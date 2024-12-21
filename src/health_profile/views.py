from django.shortcuts import render, redirect, get_object_or_404
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

        # 检查血压字段的完整性
        if (systolic_bp and not diastolic_bp) or (diastolic_bp and not systolic_bp):
            messages.error(request, "请同时填写血压的高压和低压值！")
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
            return redirect('add_health_profile')
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

@method_decorator(login_required, name='dispatch')
class delete_health_profile(View):
    def post(self, request, health_profile_id):
        health_profile = get_object_or_404(HealthProfile, id=health_profile_id, user=request.user)
        health_profile.delete()
        return redirect('health_profile_list')


@method_decorator(login_required, name='dispatch')
class health_profile_analysis(View):
    def get(self, request):
        # 获取当前用户的最新有身高记录的健康记录
        height_profile = HealthProfile.objects.filter(user=request.user).exclude(height__isnull=True).order_by('-timestamp').first()
        # 获取当前用户的最新有体重记录的健康记录
        weight_profile = HealthProfile.objects.filter(user=request.user).exclude(weight__isnull=True).order_by('-timestamp').first()

        # 初始化分析结果
        analysis_results = []

        if height_profile and weight_profile:
            # 提取最新有身高记录的身高和最新有体重记录的体重
            height = height_profile.height  # 身高 (单位: cm)
            weight = weight_profile.weight  # 体重 (单位: kg)

            # 判断身高和体重是否有效
            if height and weight:
                # 计算 BMI
                height_m = height / 100  # 转换为米
                bmi = weight / (height_m ** 2)
                bmi = round(bmi, 2)

                # 根据 BMI 设置进度条宽度和颜色
                if bmi < 18.5:
                    bmi_width = 40  # 偏瘦，宽度较小
                    bmi_color = 'danger'  # 红色，极度不正常
                elif 18.5 <= bmi < 24:
                    bmi_width = (bmi - 18.5) * 100 / 5  # 18.5到24之间，逐渐增长
                    bmi_color = 'success'  # 绿色，正常
                elif 24 <= bmi < 30:
                    bmi_width = (bmi - 24) * 100 / 6 + 50  # 超重，较高宽度
                    bmi_color = 'warning'  # 黄色，偏高
                else:
                    bmi_width = 100  # 肥胖，最大宽度
                    bmi_color = 'danger'  # 红色，极度不正常

                # 添加分析结果
                analysis_results.append({
                    'bmi': bmi,
                    'bmi_width': bmi_width,
                    'bmi_color': bmi_color,
                    'profile': height_profile  # 这里使用身高记录的健康记录
                })
            else:
                # 如果身高或体重为空
                analysis_results.append({
                    'bmi': None,
                    'bmi_width': 0,
                    'bmi_color': 'gray',  # 无数据时为灰色
                    'profile': height_profile
                })
        else:
            # 如果没有身高或体重记录
            analysis_results.append({
                'bmi': None,
                'bmi_width': 0,
                'bmi_color': 'gray',  # 无数据时为灰色
                'profile': None
            })

        return render(request, 'health_profile/health_profile_analysis.html', {
            'analysis_results': analysis_results
        })