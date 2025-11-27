from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models.project import Project
from core.models.project_analysis import ProjectAnalysis
from core.services.ai_client import generate_ai_analysis
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from core.services.security_scoring import calculate_final_security_score
from django.contrib import messages


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
1. SYSTEM ARCHITECTURE
2. THREAT MODEL (STRIDE + OWASP relevance)
3. COST ESTIMATION guidance
4. SECURE SDLC recommendations
5. SECURITY TESTING PLAN and tools
"""

    generated_text = generate_ai_analysis(prompt)

    architecture = extract_section(generated_text, "SYSTEM ARCHITECTURE")
    threat_model = extract_section(generated_text, "THREAT MODEL")
    cost_estimation = extract_section(generated_text, "COST")
    sdls_recommendations = extract_section(generated_text, "SECURE SDLC")
    testing_plan = extract_section(generated_text, "SECURITY TESTING PLAN")

    # Save initial analysis
    analysis = ProjectAnalysis.objects.create(
        project=project,
        user=request.user,
        architecture=architecture,
        threat_model=threat_model,
        cost_estimation=cost_estimation,
        sdls_recommendations=sdls_recommendations,
        testing_plan=testing_plan,
    )

    # ✅ Hybrid security scoring applied here
    score, category = calculate_final_security_score(project)
    analysis.security_score = score
    analysis.risk_category = category
    analysis.save()

    messages.success(request, f"Security analysis generated — Risk rating: {category} ({score})")

    return redirect("view_analysis", analysis_id=analysis.id)


@login_required
def view_analysis(request, analysis_id):
    analysis = get_object_or_404(ProjectAnalysis, id=analysis_id, user=request.user)
    return render(request, "core/view_analysis.html", {"analysis": analysis, "project": analysis.project})



@login_required
def history_analysis(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    analyses = ProjectAnalysis.objects.filter(project=project).order_by("-created_at")

    scores = [a.security_score for a in analyses if a.security_score > 0]

    trend_data = {
        "highest": max(scores) if scores else 0,
        "lowest": min(scores) if scores else 0,
        "average": sum(scores)/len(scores) if scores else 0,
        "improving": scores[-1] < scores[0] if len(scores) > 1 else False
    }

    return render(request, "core/analysis_history.html", {
        "project": project,
        "analyses": analyses,
        "trend": trend_data
    })


@login_required
def download_analysis_pdf(request, analysis_id):
    analysis = get_object_or_404(ProjectAnalysis, id=analysis_id, user=request.user)
    project = analysis.project

    html_content = render_to_string("core/analysis_pdf.html", {
        "analysis": analysis,
        "project": project
    })

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="analysis_{analysis_id}.pdf"'
    return response
