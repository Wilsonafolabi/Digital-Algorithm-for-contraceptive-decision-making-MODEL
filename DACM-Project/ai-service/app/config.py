import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

class Settings:
    API_KEY: str = os.getenv("API_KEY", "")
    BASE_URL: str = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
    AI_MODEL: str = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
    AI_PORT: int = int(os.getenv("AI_PORT", "8001"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    HF_ML_API_URL: str = os.getenv("HF_ML_API_URL", "https://emeritus-21-dacm-contraceptive-ml.hf.space")
    HF_ML_TIMEOUT: int = int(os.getenv("HF_ML_TIMEOUT", "10"))
    WHO_AFRICA_DATA_PATH: str = os.getenv("WHO_AFRICA_DATA_PATH", "data/who_africa_prevalence.json")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()