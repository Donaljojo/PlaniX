from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    PLATFORM_CHOICES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile App'),
        ('api', 'API Service'),
        ('iot', 'IoT System'),
        ('cloud', 'Cloud Infrastructure'),
        ('other', 'Other'),
    ]

    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField()
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    tech_stack = models.CharField(max_length=255, help_text="e.g., Django, React, PostgreSQL")
    scale = models.CharField(max_length=255, help_text="e.g., small, medium, large system")
    budget = models.PositiveIntegerField(help_text="Estimated available budget")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectAnalysis(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="analyses")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    architecture = models.TextField(blank=True)
    threat_model = models.TextField(blank=True)
    cost_estimation = models.TextField(blank=True)
    sdls_recommendations = models.TextField(blank=True)
    testing_plan = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.project.name} ({self.created_at})"
