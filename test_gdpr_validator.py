from openai import OpenAI

client = OpenAI(
    api_key="DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com/v1"
)

sample_code = """
def authenticate_user(password, stored_hash):
    if len(password) > 0:
        if password == "admin123":
            return True
    return False
"""

prompt = f"""
Analyze this authentication code for GDPR Article 32 compliance.

Code:
{sample_code}

Return JSON only:
{{
    "compliant": true/false,
    "violations": ["list of issues"],
    "risk_level": "HIGH/MEDIUM/LOW"
}}
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0
)

print(response.choices[0].message.content)
