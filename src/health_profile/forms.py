from django import forms
from .models import HealthProfile
from .models import UserCustomField

class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        fields = ['height', 'weight', 'systolic_bp', 'diastolic_bp', 'blood_sugar']

    # 这里可以添加额外的表单验证逻辑
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("身高必须为正数。")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("体重必须为正数。")
        return weight


class UserCustomFieldForm(forms.ModelForm):
    class Meta:
        model = UserCustomField
        fields = ['field_name', 'field_value']

    def clean_field_name(self):
        field_name = self.cleaned_data.get('field_name')
        if not field_name:
            raise forms.ValidationError("自定义字段名称不能为空。")
        return field_name

    def clean_field_value(self):
        field_value = self.cleaned_data.get('field_value')
        if not field_value:
            raise forms.ValidationError("自定义字段值不能为空。")
        return field_value
