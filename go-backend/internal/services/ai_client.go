package services

import (
"context"
"fmt"
"log"
"time"

"github.com/go-resty/resty/v2"
"dacm-go-backend/internal/config"
"dacm-go-backend/internal/models"
)

type AIClient struct {
client *resty.Client
}

func NewAIClient(cfg *config.Config) *AIClient {
client := resty.New().
SetBaseURL(cfg.AIServiceURL).
SetTimeout(30 * time.Second).
SetRetryCount(1).
SetRetryWaitTime(1 * time.Second)
log.Printf("?? AI Client initialized: %s", cfg.AIServiceURL)
return &AIClient{client: client}
}

func (c *AIClient) GetAdvice(ctx context.Context, req *models.AdviceRequest) (*models.AIResponse, error) {
var resp models.AIResponse
r, err := c.client.R().
SetContext(ctx).
SetBody(req).
SetResult(&resp).
Post("/api/v1/generate")

if err != nil {
log.Printf("? AI request failed: %v", err)
return nil, fmt.Errorf("ai service unreachable: %w", err)
}
if r.StatusCode() != 200 {
log.Printf("? AI service returned %d: %s", r.StatusCode(), string(r.Body()))
return nil, fmt.Errorf("ai service error: status %d", r.StatusCode())
}
log.Printf("? AI response received (confidence: %.2f)", resp.Confidence)
return &resp, nil
}

func (c *AIClient) HealthCheck(ctx context.Context) bool {
r, err := c.client.R().SetContext(ctx).Get("/health")
return err == nil && r.StatusCode() == 200
}
