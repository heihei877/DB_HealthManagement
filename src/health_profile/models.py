from django.db import models
from django.contrib.auth.models import User

class HealthProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_profiles', to_field='id')
    timestamp = models.DateTimeField(auto_now_add=True)  # 记录时间
    height = models.FloatField(null=True, blank=True)  # 身高，单位 cm
    weight = models.FloatField(null=True, blank=True)  # 体重，单位 kg
    systolic_bp = models.FloatField(null=True, blank=True)  # 血压高压
    diastolic_bp = models.FloatField(null=True, blank=True)  # 血压低压
    blood_sugar = models.FloatField(null=True, blank=True)  # 血糖，单位 mmol/L

    def __str__(self):
        return f"Health Profile for {self.user.username} at {self.timestamp}"


class UserCustomField(models.Model):
    health_profile = models.ForeignKey(HealthProfile, on_delete=models.CASCADE, related_name='custom_fields')
    field_name = models.CharField(max_length=255)  # 自定义字段的名称
    field_value = models.CharField(max_length=255)  # 自定义字段的值（可以是字符串形式，数字也可以转为字符串存储）

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"

