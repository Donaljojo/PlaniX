import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini if key exists
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

_cached_model = None


def _get_available_model():
    """
    Fetch available Gemini models and select one that supports generateContent.
    """
    global _cached_model

    if _cached_model:
        return _cached_model

    if not GEMINI_API_KEY:
        return None

    try:
        models = genai.list_models()

        preferred_order = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-pro",
            "gemini-pro-latest",
        ]

        available = [
            m.name.replace("models/", "")
            for m in models
            if "generateContent" in m.supported_generation_methods
        ]

        for model in preferred_order:
            if model in available:
                _cached_model = model
                return model

        if available:
            print(f"Available models: {available}")
            _cached_model = available[0]
            return available[0]

        print("No models available.")
        return "ERROR: No models available that support 'generateContent'."

    except Exception as e:
        print(f"Error listing models: {e}")
        return f"ERROR: Could not list models from Gemini. Details: {e}"


def generate_ai_analysis(prompt):
    """
SYSTEM ARCHITECTURE
- Multi-tier architecture with presentation, application, and data layers
- Secure API gateway enforcing authentication and rate limiting
- Encrypted data storage using industry-standard cryptography
- Logging and monitoring pipeline for audit and incident response

THREAT MODEL (STRIDE + OWASP)
- Spoofing: enforce MFA and token-based identity
- Tampering: input validation and integrity checks
- Repudiation: centralized immutable audit logs
- Information Disclosure: encryption in transit and at rest
- Denial of Service: WAF + throttling controls
- Elevation of Privilege: RBAC with least privilege principles
- OWASP Top 10 mapped to mitigation controls

SECURE SDLC PLAN
- Requirements phase includes threat modeling checkpoints
- Secure design reviews before implementation stages
- Static code analysis integrated into CI pipeline
- Dependency scanning and SBOM tracking
- Pre-deployment penetration testing
- Continuous security monitoring after release

COST ESTIMATION
- Development effort: medium complexity, 3–5 engineer months
- Hosting and infrastructure: scalable cloud deployment
- Security tooling cost ranges provided per testing model
- Optional add-on: managed security services considerations

SECURITY TESTING PLAN
- SAST, DAST, IAST, and SCA toolchain alignment
- API fuzz testing and business logic abuse detection
- Automated regression security suite
- Red-team simulation and reporting cycle
"""


    if not GEMINI_API_KEY:
        return "ERROR: No Gemini API key configured."

    model_name = _get_available_model()

    if not model_name or model_name.startswith("ERROR:"):
        return model_name or "ERROR: No supported Gemini model available. Please ensure your API key is correct and that you have access to a model that supports 'generateContent'."

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "ERROR: No text response from model."

    except Exception as e:
        return f"AI Error: {str(e)}"
