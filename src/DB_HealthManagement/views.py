from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from exercise_info.models import ExerciseGoal


def cover(request):
    return render(request, 'cover.html')

def about(request):
    return render(request, 'about.html')

def contact_us(request):
    return render(request, 'contact_us.html')

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def get_exercise_goals(request):
    # 查询当前用户的运动目标
    goals = ExerciseGoal.objects.filter(user_id=request.user.id)
    events = []

    for goal in goals:
        events.append({
            "id": goal.exercise_goal_id,
            "title": f"{goal.type} - {goal.target_calorie_cost} kcal",
            "start": goal.start_time.isoformat(),
            "end": goal.end_time.isoformat(),
            "className": "success"  # 可以根据实际需求动态设置样式
        })

    return JsonResponse(events, safe=False)