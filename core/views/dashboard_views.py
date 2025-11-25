from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Project

@login_required
def dashboard(request):
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "core/dashboard.html", {"projects": projects})
