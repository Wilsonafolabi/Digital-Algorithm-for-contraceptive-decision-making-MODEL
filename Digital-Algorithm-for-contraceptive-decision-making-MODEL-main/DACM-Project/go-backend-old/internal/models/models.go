package models
type UserProfile struct { Age int `json:"age" binding:"required,min=12,max=55"`; Conditions []string `json:"conditions"`; CurrentMethod string `json:"current_method"`; SmokingStatus string `json:"smoking_status" binding:"oneof=non-smoker smoker former-smoker"`; BMI *float64 `json:"bmi,omitempty"` }
type Req struct { Query string `json:"query" binding:"required,min=5,max=800"`; UserProfile UserProfile `json:"user_profile" binding:"required"` }
type Route struct { ToCounselor bool `json:"routed_to_counselor"`; Reason string `json:"reason,omitempty"`; Endpoint string `json:"counselor_endpoint,omitempty"` }
type Src struct { Title, Category string; Score float64 `json:"relevance_score"` }
type Safe struct { Flagged bool; Reason, WhoCat, Action string `json:"reason,omitempty" json:"who_category,omitempty" json:"action_required"` }
type Res struct { Route Route `json:"routing"`; Ans string `json:"answer"`; Conf float64 `json:"confidence"`; Srcs []Src `json:"sources"`; Safe Safe `json:"safety"`; Sug, Con []string `json:"suggested_methods" json:"contraindicated_methods"` }
