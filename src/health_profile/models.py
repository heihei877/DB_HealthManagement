from django.db import models
from django.contrib.auth.models import User

class HealthProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_profiles')
    height = models.FloatField(null=True, blank=True)  # 身高，单位为厘米
    weight = models.FloatField(null=True, blank=True)  # 体重，单位为千克
    blood_sugar = models.FloatField(null=True, blank=True)  # 血糖
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)  # 血压，格式如 '120/80'
    custom_fields = models.JSONField(default=dict, blank=True)  # 用户自定义字段，存储为 JSON 格式

    def __str__(self):
        return f"{self.user.username}'s Health Profile"

    class Meta:
        ordering = ['-id']  # 按照创建时间倒序排列
