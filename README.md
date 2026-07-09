# DACM - Digital Algorithm For Contraceptive Decision-Making
## Quick Start
1. `cd ai-service` → edit `.env` → `pip install -r requirements.txt` → `uvicorn app.main:app --port 8001 --reload`
2. `cd go-backend` → `go mod tidy` → `go run cmd/main.go`
3. Test: `curl -X POST http://localhost:8000/api/v1/advice -H "Content-Type: application/json" -d '{"query":"Is the pill safe?","user_profile":{"age":37,"conditions":[],"current_method":"None","smoking_status":"smoker"}}'`

## Provider Setup
Edit `ai-service/.env`:
- **Gemini**: `BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/` | `AI_MODEL=gemini-2.0-flash`
- **Qwen**: `BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1` | `AI_MODEL=qwen-turbo`
- **Groq**: `BASE_URL=https://api.groq.com/openai/v1` | `AI_MODEL=llama3-8b-8192`
- **OpenAI/Grok**: Change `BASE_URL` & `AI_MODEL` accordingly.
No code changes needed. Just restart the Python service.
