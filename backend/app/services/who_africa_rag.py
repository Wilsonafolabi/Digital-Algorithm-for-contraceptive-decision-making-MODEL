import json
from pathlib import Path
from app.config import settings

class WhoAfricaRAG:
    def __init__(self):
        base_dir = Path(__file__).resolve().parents[2]  # ai-service/
        path = base_dir / settings.WHO_AFRICA_DATA_PATH
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.docs = json.load(f)
            print(f"✅ WHO Africa RAG loaded: {len(self.docs)} records")
        except Exception as e:
            print(f"⚠️ WHO Africa data not found at {path}: {e}")
            self.docs = []

    def search(self, country_iso3: str = None, top_k: int = 3) -> list:
        results = self.docs
        if country_iso3:
            results = [d for d in results if d["metadata"]["country_iso3"].lower() == country_iso3.lower()]
        results = sorted(results, key=lambda x: (-x["metadata"]["year"], -x["metadata"]["prevalence_percent"]))
        return results[:top_k]