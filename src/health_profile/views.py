from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import HealthProfile
from .forms import HealthProfileForm

@login_required
def health_profile_list(request):
    # 获取当前用户的所有健康记录
    profiles = HealthProfile.objects.filter(user=request.user)
    return render(request, 'health_profile/health_profile_list.html', {'profiles': profiles})

@login_required
def add_health_profile(request):
    if request.method == 'POST':
        form = HealthProfileForm(request.POST)
        if form.is_valid():
            # 设置健康记录的用户
            health_profile = form.save(commit=False)
            health_profile.user = request.user
            health_profile.save()
            return redirect('health_profile_list')
    else:
        form = HealthProfileForm()
    return render(request, 'health_profile/add_health_profile.html', {'form': form})

@login_required
def delete_health_profile(request, profile_id):
    health_profile = get_object_or_404(HealthProfile, id=profile_id, user=request.user)
    health_profile.delete()
    return redirect('health_profile_list')
