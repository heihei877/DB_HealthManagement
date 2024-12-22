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
        # 获取当前用户的最新健康记录（身高、体重、血压、血糖）
        height_profile = HealthProfile.objects.filter(user=request.user).exclude(height__isnull=True).order_by('-timestamp').first()
        weight_profile = HealthProfile.objects.filter(user=request.user).exclude(weight__isnull=True).order_by('-timestamp').first()
        blood_pressure_profile = HealthProfile.objects.filter(user=request.user).exclude(systolic_bp__isnull=True).exclude(diastolic_bp__isnull=True).order_by('-timestamp').first()
        blood_glucose_profile = HealthProfile.objects.filter(user=request.user).exclude(blood_sugar__isnull=True).order_by('-timestamp').first()

        # 初始化分析结果
        analysis_bmi_result = []
        analysis_bp_result = []
        analysis_bg_result = []

        # 身高和体重分析（BMI）
        if height_profile and weight_profile:
            height = height_profile.height  # 身高 (单位: cm)
            weight = weight_profile.weight  # 体重 (单位: kg)
            if height and weight:
                height_m = height / 100  # 转换为米
                bmi = weight / (height_m ** 2)
                bmi = float(round(bmi, 2))

                # 根据BMI设置进度条
                if bmi < 18.5:
                    bmi_width = 40
                    bmi_color = 'danger'
                elif 18.5 <= bmi < 24:
                    bmi_width = (bmi - 18.5) * 100 / 5
                    bmi_color = 'success'
                elif 24 <= bmi < 30:
                    bmi_width = (bmi - 24) * 100 / 6 + 50
                    bmi_color = 'warning'
                else:
                    bmi_width = 100
                    bmi_color = 'danger'

                analysis_bmi_result.append({
                    'bmi': bmi,
                    'bmi_width': bmi_width,
                    'bmi_color': bmi_color,
                })
            else:
                analysis_bmi_result.append({
                    'bmi': None,
                    'bmi_width': 0,
                    'bmi_color': 'gray',
                })
        else:
            analysis_bmi_result.append({
                'bmi': None,
                'bmi_width': 0,
                'bmi_color': 'gray',
            })

        # 血压分析
        if blood_pressure_profile:
            systolic_bp = blood_pressure_profile.systolic_bp
            diastolic_bp = blood_pressure_profile.diastolic_bp

            if systolic_bp and diastolic_bp:
                if systolic_bp < 90 or diastolic_bp < 60:
                    bp_status = 'hypotension'
                    bp_width = 20
                    bp_color = 'danger'
                elif 90 <= systolic_bp < 120 and 60 <= diastolic_bp < 80:
                    bp_status = 'normal'
                    bp_width = 40
                    bp_color = 'success'
                elif 120 <= systolic_bp < 140 or 80 <= diastolic_bp < 90:
                    bp_status = 'prehypertension'
                    bp_width = 60
                    bp_color = 'warning'
                elif 140 <= systolic_bp < 160 or 90 <= diastolic_bp < 100:
                    bp_status = 'hypertension_stage_1'
                    bp_width = 80
                    bp_color = 'warning'
                elif 160 <= systolic_bp < 180 or 100 <= diastolic_bp < 110:
                    bp_status = 'hypertension_stage_2'
                    bp_width = 90
                    bp_color = 'danger'
                else:
                    bp_status = 'hypertensive_crisis'
                    bp_width = 100
                    bp_color = 'danger'

                analysis_bp_result.append({
                    'bp_status': bp_status,
                    'bp_width': bp_width,
                    'bp_color': bp_color,
                    'systolic_bp': systolic_bp,
                    'diastolic_bp': diastolic_bp,
                })
            else:
                analysis_bp_result.append({
                    'bp_status': None,
                    'bp_width': 0,
                    'bp_color': 'gray',
                })
        else:
            analysis_bp_result.append({
                'bp_status': None,
                'bp_width': 0,
                'bp_color': 'gray',
            })

        # 血糖分析
        if blood_glucose_profile:
            blood_glucose = blood_glucose_profile.blood_sugar  # 血糖值 (单位: mmol/L)
            if blood_glucose:
                if blood_glucose < 3.9:
                    glucose_status = 'hypoglycemia'
                    glucose_width = 20
                    glucose_color = 'danger'
                elif 3.9 <= blood_glucose < 5.6:
                    glucose_status = 'normal'
                    glucose_width = 40
                    glucose_color = 'success'
                elif 5.6 <= blood_glucose < 7.8:
                    glucose_status = 'prediabetes'
                    glucose_width = 60
                    glucose_color = 'warning'
                else:
                    glucose_status = 'diabetes'
                    glucose_width = 80
                    glucose_color = 'danger'

                analysis_bg_result.append({
                    'glucose_status': glucose_status,
                    'glucose_width': glucose_width,
                    'glucose_color': glucose_color,
                    'blood_glucose': blood_glucose,
                })
            else:
                analysis_bg_result.append({
                    'glucose_status': None,
                    'glucose_width': 0,
                    'glucose_color': 'gray',
                })
        else:
            analysis_bg_result.append({
                'glucose_status': None,
                'glucose_width': 0,
                'glucose_color': 'gray',
            })

        return render(request, 'health_profile/health_profile_analysis.html', {
            'analysis_bmi_result': analysis_bmi_result,
            'analysis_bp_result': analysis_bp_result,
            'analysis_bg_result': analysis_bg_result,
        })
