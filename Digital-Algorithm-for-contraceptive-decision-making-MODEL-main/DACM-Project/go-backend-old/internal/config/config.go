package config

import (
	"log"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	Port         string
	Env          string
	AIServiceURL string
	CORSOrigins  []string
	LogLevel     string
}

var C *Config

func Load() *Config {
	// Load .env from go-backend root
	if err := godotenv.Load(); err != nil {
		log.Println("⚠️ .env not found, using defaults")
	}

	C = &Config{
		Port:         getEnv("PORT", "8000"),
		Env:          getEnv("ENV", "development"),
		AIServiceURL: getEnv("AI_SERVICE_URL", "http://localhost:8001"),
		CORSOrigins:  strings.Split(getEnv("CORS_ORIGINS", "http://localhost:3000"), ","),
		LogLevel:     getEnv("LOG_LEVEL", "info"),
	}

	log.Printf("✅ Config loaded: AI_SERVICE_URL=%s, PORT=%s", C.AIServiceURL, C.Port)
	return C
}

func getEnv(key, defaultVal string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return defaultVal
}
