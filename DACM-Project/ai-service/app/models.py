from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class UserProfile(BaseModel):
    age: int
    country_iso3: Optional[str] = None
    breastfeeding: bool = False
    hypertension: bool = False
    smoking_status: str = "non-smoker"
    history_of_clots: bool = False
    migraines: str = "none"  # none, without_aura, with_aura
    diabetes: bool = False
    pregnancy_intention: str = "delay"  # delay, space, complete
    previous_method: Optional[str] = None
    side_effects_history: Optional[str] = None
    sti_protection_needed: bool = False
    number_of_children: Optional[int] = None

class GenerateRequest(BaseModel):
    query: str
    user_profile: UserProfile

class GuidelineSource(BaseModel):
    title: str
    category: str
    content: str
    relevance_score: float

class SafetyAssessment(BaseModel):
    flagged: bool
    risk_category: str
    message: str

class BehavioralInsight(BaseModel):
    satisfaction_probability: float
    interpretation: str
    recommendation: str

class AIResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[GuidelineSource]
    safety: SafetyAssessment
    suggested_methods: List[str]
    contraindicated_methods: List[str]
    behavioral_insight: Optional[BehavioralInsight] = None
    regional_context: Optional[List[Dict]] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)