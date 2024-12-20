from django import forms
from .models import ExerciseRecord

class ExerciseRecordForm(forms.ModelForm):
    class Meta:
        model = ExerciseRecord
        fields = ['type', 'start_time', 'end_time', 'calorie_cost']  # 指定要填写的字段
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
