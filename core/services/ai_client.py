import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_ai_analysis(prompt):
    if not GROQ_API_KEY:
        return "ERROR: No GROQ API key configured."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama3-8b-8192",  # ✅ confirmed working model
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in secure software architecture, threat modeling "
                    "(STRIDE and OWASP), secure SDLC planning, security testing methodology, "
                    "and cost estimation for secure development projects."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"API Error: {response.text}"



