from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms import ProjectForm

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect("dashboard")
    else:
        form = ProjectForm()

    return render(request, "core/create_project.html", {"form": form})
