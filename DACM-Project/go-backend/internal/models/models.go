package models

type UserProfile struct {
	Age                 int     `json:"age"`
	CountryISO3         *string `json:"country_iso3,omitempty"`
	Breastfeeding       bool    `json:"breastfeeding"`
	Hypertension        bool    `json:"hypertension"`
	SmokingStatus       string  `json:"smoking_status"`
	HistoryOfClots      bool    `json:"history_of_clots"`
	Migraines           string  `json:"migraines"`
	Diabetes            bool    `json:"diabetes"`
	PregnancyIntention  string  `json:"pregnancy_intention"`
	PreviousMethod      *string `json:"previous_method,omitempty"`
	SideEffectsHistory  *string `json:"side_effects_history,omitempty"`
	STIProtectionNeeded bool    `json:"sti_protection_needed"`
	NumberOfChildren    *int    `json:"number_of_children,omitempty"`
}

type AdviceRequest struct {
	Query       string      `json:"query" binding:"required"`
	UserProfile UserProfile `json:"user_profile" binding:"required"`
}

type GuidelineSource struct {
	Title          string  `json:"title"`
	Category       string  `json:"category"`
	Content        string  `json:"content"`
	RelevanceScore float64 `json:"relevance_score"`
}

type SafetyAssessment struct {
	Flagged      bool   `json:"flagged"`
	RiskCategory string `json:"risk_category"`
	Message      string `json:"message"`
}

type BehavioralInsight struct {
	SatisfactionProbability float64 `json:"satisfaction_probability"`
	Interpretation          string  `json:"interpretation"`
	Recommendation          string  `json:"recommendation"`
}

type AIResponse struct {
	Answer                 string             `json:"answer"`
	Confidence             float64            `json:"confidence"`
	Sources                []GuidelineSource  `json:"sources"`
	Safety                 SafetyAssessment   `json:"safety"`
	SuggestedMethods       []string           `json:"suggested_methods"`
	ContraindicatedMethods []string           `json:"contraindicated_methods"`
	BehavioralInsight      *BehavioralInsight `json:"behavioral_insight,omitempty"`
	RegionalContext        []map[string]any   `json:"regional_context,omitempty"`
	GeneratedAt            string             `json:"generated_at"`
}

type APIResponse struct {
	Success bool        `json:"success"`
	Data    *AIResponse `json:"data,omitempty"`
	Error   *string     `json:"error,omitempty"`
}
