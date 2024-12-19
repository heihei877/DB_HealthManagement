from django import forms
from .models import HealthProfile

class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        fields = ['height', 'weight', 'blood_sugar', 'blood_pressure', 'custom_fields']
        widgets = {
            'custom_fields': forms.Textarea(attrs={'rows': 3, 'placeholder': '请输入自定义字段的JSON格式'}),  # 提供一个多行文本框用于输入 JSON
        }

    def clean_custom_fields(self):
        custom_fields = self.cleaned_data.get('custom_fields', {})
        if isinstance(custom_fields, str):
            try:
                import json
                custom_fields = json.loads(custom_fields)
            except json.JSONDecodeError:
                raise forms.ValidationError("自定义字段格式不正确，请提供有效的JSON格式")
        return custom_fields
