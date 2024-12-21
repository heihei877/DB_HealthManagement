from django import forms
from .models import HealthProfile

class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        fields = ['height', 'weight', 'blood_pressure', 'blood_sugar']
