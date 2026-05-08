import os
import sys
import json
from openai import OpenAI

class GDPRArticle32Validator:
    def __init__(self):
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not api_key:
            print("ERROR: DEEPSEEK_API_KEY not set")
            sys.exit(1)
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    
    def validate_article_32(self, code):
        prompt = f"""
        Analyze this code for GDPR Article 32 compliance.
        
        Article 32 requires:
        1. Pseudonymization and encryption of personal data
        2. Ongoing confidentiality of systems
        3. Ability to restore availability after incidents
        4. Regular testing of security measures
        
        Code:
        {code[:3000]}
        
        Return ONLY valid JSON:
        {{
            "compliant": true/false,
            "violations": ["violation1", "violation2"],
            "risk_level": "HIGH/MEDIUM/LOW",
            "remediation_steps": ["step1", "step2"]
        }}
        """
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content)

def main():
    validator = GDPRArticle32Validator()
    with open('src/app.py', 'r') as f:
        code = f.read()
    
    result = validator.validate_article_32(code)
    
    print(json.dumps(result, indent=2))
    
    with open('compliance_result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    if not result.get('compliant', False):
        print("\nDEPLOYMENT BLOCKED: GDPR Article 32 non-compliant")
        sys.exit(1)
    
    print("\nGDPR Article 32 compliance validated")
    sys.exit(0)

if __name__ == "__main__":
    main()
