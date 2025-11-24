from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'platform',
            'tech_stack',
            'scale',
            'budget',
            'risk_level',
        ]
