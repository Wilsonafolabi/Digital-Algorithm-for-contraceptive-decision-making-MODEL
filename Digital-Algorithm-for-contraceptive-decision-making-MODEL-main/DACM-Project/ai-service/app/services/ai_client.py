from openai import OpenAI
from app.config import get_settings
s = get_settings()
class AIClient:
    SYS = """You are a clinical contraceptive advisor trained on WHO Medical Eligibility Criteria (MEC).
RULES: 1. Cite WHO MEC Categories. 2. Never diagnose/prescribe. 3. Flag Category 3/4 for provider consult.
4. Use clear, respectful language. 5. Ask 1 clarifying question if info is missing."""
    def __init__(self):
        self.client = OpenAI(api_key=s.api_key, base_url=s.base_url)
        self.model = s.ai_model
        print(f"✅ AI initialized: {s.ai_model} via {s.base_url}")
    def generate(self, prompt: str) -> str:
        return self.client.chat.completions.create(model=self.model, messages=[{"role":"user","content":prompt}], temperature=0.2, max_tokens=500).choices[0].message.content.strip()
