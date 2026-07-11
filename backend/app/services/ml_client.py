import requests
from app.config import settings

class HFMLClient:
    def __init__(self):
        self.url = f"{settings.HF_ML_API_URL}/predict"
        self.timeout = settings.HF_ML_TIMEOUT

    def predict(self, query: str, useful_count: int = 0) -> dict:
        try:
            resp = requests.post(self.url, json={"query": query, "useful_count": useful_count}, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"⚠️ HF ML prediction failed: {e}")
            return {"satisfaction_probability": 0.0, "interpretation": "unknown", "recommendation": "proceed"}