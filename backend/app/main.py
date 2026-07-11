from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import httpx
import os

from app.config import settings
from app.models import GenerateRequest, AIResponse, GuidelineSource, SafetyAssessment, BehavioralInsight
from app.services.ml_client import HFMLClient
from app.services.who_africa_rag import WhoAfricaRAG
from app.services.safety_engine import SafetyEngine
from app.services.rag_service import RAGService

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("✅ DACM AI Service ready (lazy loading enabled)")
    yield

def get_ml_client(app):
    if not hasattr(app.state, 'ml') or app.state.ml is None:
        app.state.ml = HFMLClient()
    return app.state.ml

def get_who_africa(app):
    if not hasattr(app.state, 'who_africa') or app.state.who_africa is None:
        app.state.who_africa = WhoAfricaRAG()
    return app.state.who_africa

def get_safety(app):
    if not hasattr(app.state, 'safety') or app.state.safety is None:
        app.state.safety = SafetyEngine()
    return app.state.safety

def get_rag(app):
    if not hasattr(app.state, 'rag') or app.state.rag is None:
        app.state.rag = RAGService()
    return app.state.rag

app = FastAPI(title="DACM AI", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/api/v1/advice", response_model=AIResponse)
async def generate(req: GenerateRequest):
    safety = get_safety(app).check(req.user_profile.dict())
    if safety["flagged"] and safety["risk_category"] == "critical":
        return AIResponse(
            answer=safety["message"], confidence=1.0, sources=[],
            safety=SafetyAssessment(**safety), suggested_methods=[], contraindicated_methods=[]
        )

    guidelines = get_rag(app).search(req.query, req.user_profile.dict(), k=2)
    rag_context = "\n".join([f"[{g['category']}] {g['title']}: {g['content']}" for g in guidelines])

    regional_context = []
    regional_text = ""
    if req.user_profile.country_iso3:
        regional_context = get_who_africa(app).search(country_iso3=req.user_profile.country_iso3, top_k=2)
        if regional_context:
            regional_text = "\n\n🌍 Regional Context: " + "; ".join([f"{d['metadata']['method']} ({d['metadata']['prevalence_percent']}%)" for d in regional_context])

    ml_result = {}
    try:
        ml_result = get_ml_client(app).predict(req.query)
    except Exception as e:
        logger.warning(f"ML fallback: {e}")

    prompt = f"""CLINICAL GUIDELINES (WHO MEC):
{rag_context}

USER CLINICAL PROFILE:
- Age: {req.user_profile.age}
- Breastfeeding: {req.user_profile.breastfeeding}
- Hypertension: {req.user_profile.hypertension}
- Smoking: {req.user_profile.smoking_status}
- Blood Clots History: {req.user_profile.history_of_clots}
- Migraines: {req.user_profile.migraines}
- Diabetes: {req.user_profile.diabetes}
- Pregnancy Intention: {req.user_profile.pregnancy_intention}
- Previous Method: {req.user_profile.previous_method or 'None'}
- Side Effects History: {req.user_profile.side_effects_history or 'None'}
- STI Protection Needed: {req.user_profile.sti_protection_needed}
- Number of Children: {req.user_profile.number_of_children or 'Not specified'}
- Country: {req.user_profile.country_iso3 or 'N/A'}

QUERY: {req.query}

INSTRUCTIONS: Provide a clear, medically accurate contraceptive recommendation based strictly on WHO MEC guidelines. Prioritize safety contraindications first. Address STI needs if flagged. Align suggestions with pregnancy intention. Cite specific MEC categories. Keep response empathetic and professional."""

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{settings.BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {settings.API_KEY}", "Content-Type": "application/json"},
                json={"model": settings.AI_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
            )
            resp.raise_for_status()
            llm_answer = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        llm_answer = "Based on WHO guidelines, please consult a healthcare provider for personalized contraceptive advice."

    answer = llm_answer + regional_text
    if ml_result.get("satisfaction_probability", 0) > 0.7:
        answer += f"\n\n💡 User Experience Insight: {ml_result['interpretation'].capitalize()} predicted satisfaction ({ml_result['satisfaction_probability']*100:.0f}%) based on similar user reviews."

    sources_list = [GuidelineSource(**g) for g in guidelines]
    if regional_context:
        for d in regional_context:
            sources_list.append(GuidelineSource(title=d["title"], category="WHO Africa Prevalence", content="", relevance_score=0.6))

    contraindicated = []
    if any(g["category"] in ["WHO MEC 3", "WHO MEC 4"] for g in guidelines):
        contraindicated.append("combined_hormonal_methods")

    return AIResponse(
        answer=answer,
        confidence=0.85,
        sources=sources_list,
        safety=SafetyAssessment(**safety),
        suggested_methods=["progestin_only_pill", "implant", "copper_iud", "condoms"],
        contraindicated_methods=contraindicated,
        behavioral_insight=BehavioralInsight(**ml_result) if ml_result and "satisfaction_probability" in ml_result else None,
        regional_context=regional_context if regional_context else None
    )

@app.get("/health")
def health():
    return {"status": "ok", "services": ["rag", "safety", "ml", "who_africa"]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.AI_PORT))
    uvicorn.run("app.main:app", host=settings.HOST, port=port, reload=True)
