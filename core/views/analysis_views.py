from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Project, ProjectAnalysis
from core.services.ai_client import generate_ai_analysis


@login_required
def generate_analysis(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    prompt = f"""
    Generate a secure system analysis for:
    Name: {project.name}
    Description: {project.description}
    Platform: {project.platform}
    Tech Stack: {project.tech_stack}
    Scale: {project.scale}
    Budget: {project.budget}
    Risk Level: {project.risk_level}

    Provide:
    1. System architecture
    2. Threat model (STRIDE + OWASP relevance)
    3. Cost estimation guidance
    4. Recommended secure SDLC practices
    5. Security testing plan and tool recommendations
    """

    result = generate_ai_analysis(prompt)

    analysis = ProjectAnalysis.objects.create(
        project=project,
        user=request.user,
        architecture=result,
        threat_model="Included in result",
        cost_estimation="Included in result",
        sdls_recommendations="Included in result",
        testing_plan="Included in result",
    )

    return redirect("view_analysis", analysis_id=analysis.id)


@login_required
def view_analysis(request, analysis_id):
    analysis = get_object_or_404(ProjectAnalysis, id=analysis_id, user=request.user)
    return render(request, "core/view_analysis.html", {"analysis": analysis})



