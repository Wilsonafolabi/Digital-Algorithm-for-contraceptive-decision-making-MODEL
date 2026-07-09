package config

import (
"log"
"os"
"strings"

"github.com/joho/godotenv"
)

type Config struct {
Port         string
AIServiceURL string
CORSOrigins  []string
Env          string
}

func Load() *Config {
_ = godotenv.Load()
cfg := &Config{
Port:         getEnv("PORT", "8000"),
AIServiceURL: getEnv("AI_SERVICE_URL", "http://localhost:8001"),
CORSOrigins:  strings.Split(getEnv("CORS_ORIGINS", "*"), ","),
Env:          getEnv("ENV", "development"),
}
log.Printf("? Config loaded: AI_URL=%s, PORT=%s", cfg.AIServiceURL, cfg.Port)
return cfg
}

func getEnv(key, fallback string) string {
if v := os.Getenv(key); v != "" {
return v
}
return fallback
}
