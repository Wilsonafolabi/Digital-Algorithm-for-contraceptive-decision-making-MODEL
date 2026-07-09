package handlers

import (
"log"
"net/http"

"github.com/gin-gonic/gin"
"dacm-go-backend/internal/models"
"dacm-go-backend/internal/services"
)

type AdviceHandler struct {
ai *services.AIClient
}

func NewAdviceHandler(ai *services.AIClient) *AdviceHandler {
return &AdviceHandler{ai: ai}
}

func (h *AdviceHandler) GetAdvice(c *gin.Context) {
var req models.AdviceRequest
if err := c.ShouldBindJSON(&req); err != nil {
c.JSON(http.StatusBadRequest, models.APIResponse{Success: false, Error: strPtr("Invalid request format")})
return
}

country := "N/A"
if req.UserProfile.CountryISO3 != nil {
country = *req.UserProfile.CountryISO3
}
log.Printf("?? Request: age=%d, country=%s", req.UserProfile.Age, country)

resp, err := h.ai.GetAdvice(c.Request.Context(), &req)
if err != nil {
log.Printf("?? AI fallback triggered: %v", err)
c.JSON(http.StatusServiceUnavailable, models.APIResponse{
Success: false,
Error:   strPtr("AI service temporarily unavailable. Please try again."),
})
return
}

c.JSON(http.StatusOK, models.APIResponse{Success: true, Data: resp})
}

func (h *AdviceHandler) HealthCheck(c *gin.Context) {
if h.ai.HealthCheck(c.Request.Context()) {
c.JSON(http.StatusOK, gin.H{"status": "healthy", "ai_service": "connected"})
} else {
c.JSON(http.StatusServiceUnavailable, gin.H{"status": "degraded", "ai_service": "disconnected"})
}
}

func strPtr(s string) *string { return &s }
