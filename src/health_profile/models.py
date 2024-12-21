from django.db import models
from django.contrib.auth.models import User


class HealthProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_profiles', to_field='id')
    timestamp = models.DateTimeField(auto_now_add=True)  # 记录时间
    height = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)  # 身高，单位 cm
    weight = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)  # 体重，单位 kg
    systolic_bp = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)  # 血压高压
    diastolic_bp = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)  # 血压低压
    blood_sugar = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)  # 血糖，单位 mmol/L

    def __str__(self):
        return f"Health Profile for {self.user.username} at {self.timestamp}"
