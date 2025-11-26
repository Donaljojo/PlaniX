from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models.project import Project
from core.models.project_analysis import ProjectAnalysis
from core.services.ai_client import generate_ai_analysis


def extract_section(text, header):
    if header not in text:
        return ""
    section = text.split(header, 1)[1]
    for next_header in [
        "THREAT MODEL",
        "SECURE SDLC",
        "COST",
        "SECURITY TESTING PLAN"
    ]:
        if next_header in section and header not in next_header:
            section = section.split(next_header, 1)[0]
            break
    return section.strip()


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

    architecture = extract_section(result, "SYSTEM ARCHITECTURE")
    threat_model = extract_section(result, "THREAT MODEL")
    sdls_recommendations = extract_section(result, "SECURE SDLC")
    cost_estimation = extract_section(result, "COST")
    testing_plan = extract_section(result, "SECURITY TESTING PLAN")

    analysis = ProjectAnalysis.objects.create(
        project=project,
        user=request.user,
        architecture=architecture,
        threat_model=threat_model,
        sdls_recommendations=sdls_recommendations,
        cost_estimation=cost_estimation,
        testing_plan=testing_plan,
    )

    return redirect("view_analysis", analysis_id=analysis.id)


@login_required
def view_analysis(request, analysis_id):
    analysis = get_object_or_404(ProjectAnalysis, id=analysis_id, user=request.user)
    return render(request, "core/view_analysis.html", {"analysis": analysis, "project": analysis.project})


@login_required
def history_analysis(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    analyses = project.analyses.all().order_by("-created_at")
    return render(request, "core/analysis_history.html", {"project": project, "analyses": analyses})



