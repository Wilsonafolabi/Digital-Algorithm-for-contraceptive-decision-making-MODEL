package main

import (
"log"
"net/http"
"time"

"github.com/gin-gonic/gin"
"dacm-go-backend/internal/config"
"dacm-go-backend/internal/handlers"
"dacm-go-backend/internal/services"
)

func main() {
cfg := config.Load()
if cfg.Env == "production" {
gin.SetMode(gin.ReleaseMode)
}

aiClient := services.NewAIClient(cfg)
handler := handlers.NewAdviceHandler(aiClient)

r := gin.Default()
r.Use(corsMiddleware(cfg.CORSOrigins))

api := r.Group("/api/v1")
api.POST("/advice", handler.GetAdvice)
api.GET("/health", handler.HealthCheck)

r.GET("/", func(c *gin.Context) {
c.JSON(http.StatusOK, gin.H{
"service":  "DACM Go Backend",
"version":  "1.0.0",
"endpoint": "/api/v1/advice",
})
})

addr := ":" + cfg.Port
log.Printf("?? Go backend starting on http://localhost%s", addr)

srv := &http.Server{
Addr:         addr,
Handler:      r,
ReadTimeout:  15 * time.Second,
WriteTimeout: 30 * time.Second,
}

if err := srv.ListenAndServe(); err != nil {
log.Fatalf("? Server failed: %v", err)
}
}

func corsMiddleware(origins []string) gin.HandlerFunc {
return func(c *gin.Context) {
origin := c.GetHeader("Origin")
allow := "*"
if len(origins) > 0 && origins[0] != "*" {
for _, o := range origins {
if o == origin {
allow = origin
break
}
}
}
c.Header("Access-Control-Allow-Origin", allow)
c.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")
if c.Request.Method == "OPTIONS" {
c.AbortWithStatus(204)
return
}
c.Next()
}
}
