from core.models.project import Project
from core.services.ai_client import generate_ai_analysis


def calculate_rule_score(project: Project):
    score = 0

    # --- Risk level weight ---
    risk_weights = {
        "low": 10,
        "medium": 40,
        "high": 70
    }
    score += risk_weights.get(project.risk_level, 20)

    # --- Platform exposure weighting ---
    platform_weights = {
        "api": 20,
        "cloud": 20,
        "iot": 25,
        "mobile": 10,
        "web": 10,
        "other": 5
    }
    score += platform_weights.get(project.platform, 5)

    # --- Scale weighting ---
    scale_weights = {
        "small": 5,
        "medium": 10,
        "large": 20
    }
    score += scale_weights.get(project.scale.lower(), 10)

    # --- Budget adequacy scoring ---
    expected_budget = 0
    if project.scale.lower() == "small":
        expected_budget = 20000
    elif project.scale.lower() == "medium":
        expected_budget = 50000
    elif project.scale.lower() == "large":
        expected_budget = 120000

    if project.budget < expected_budget:
        score += 20  # underfunded increases risk
    else:
        score -= 10  # adequate budget reduces risk

    # Clamp baseline score range
    return max(0, min(score, 100))


def get_ai_risk_adjustment(project: Project):
    prompt = f"""
Rate the security risk severity of this system on a scale from 1 to 10.
Return ONLY a number, no words.

System Details:
Name: {project.name}
Description: {project.description}
Platform: {project.platform}
Tech Stack: {project.tech_stack}
Risk Level: {project.risk_level}
Scale: {project.scale}
Budget: {project.budget}
"""

    response = generate_ai_analysis(prompt)

    # Ensure AI returns numeric value
    try:
        ai_value = int("".join(filter(str.isdigit, response)))
        return max(0, min(ai_value, 10))
    except:
        return 0  # fallback if AI fails


def determine_risk_category(score: int):
    if score >= 70:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    return "Low Risk"


def calculate_final_security_score(project: Project):
    base_score = calculate_rule_score(project)
    ai_adjustment = get_ai_risk_adjustment(project)

    final_score = base_score + (ai_adjustment * 2)

    # final hard clamp
    if final_score > 100:
        final_score = 100
    if final_score < 0:
        final_score = 0

    category = determine_risk_category(final_score)

    return final_score, category
