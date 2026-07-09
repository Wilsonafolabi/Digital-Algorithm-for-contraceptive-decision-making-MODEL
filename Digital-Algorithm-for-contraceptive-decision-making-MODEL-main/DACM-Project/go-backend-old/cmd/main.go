package main

import (
	"dacm-go/internal/client"
	"dacm-go/internal/config"
	"dacm-go/internal/handlers"
	"log"

	"github.com/gin-gonic/gin"
)

func main() {
	cfg := config.Load()
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	r.Use(func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", cfg.CORS)
		c.Header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Content-Type")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	})

	h := handlers.H{AI: client.New(cfg.AIURL)}
	v1 := r.Group("/api/v1")
	{
		v1.POST("/advice", h.Advice)
		v1.GET("/counseling/book", func(c *gin.Context) {
			c.JSON(200, gin.H{"msg": "Booking endpoint for adolescent counseling"})
		})
	}

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	log.Printf("🚀 DACM running on :%s", cfg.Port)
	log.Fatal(r.Run(":" + cfg.Port))
}
