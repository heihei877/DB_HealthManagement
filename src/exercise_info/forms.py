from django import forms
from .models import ExerciseRecord, ExerciseGoal

class ExerciseRecordForm(forms.ModelForm):
    class Meta:
        model = ExerciseRecord
        fields = ['type', 'start_time', 'end_time', 'calorie_cost']  # 指定要填写的字段
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ExerciseGoalForm(forms.ModelForm):
    class Meta:
        model = ExerciseGoal
        fields = ['type', 'start_time', 'end_time', 'target_calorie_cost']

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }