# Medical FAQ Chatbot

A HIPAA-aware medical FAQ chatbot, autonomously built by [my-agent-hub](https://github.com/rajaganaa/spec-driven-multi-ai-agents-) — a spec-driven multi-agent coding system — from a single plain-English goal.

## Stack
- Backend: FastAPI + SQLAlchemy (SQLite for local dev, PostgreSQL-ready)
- Frontend: React

## Setup

**Backend:**
```bash
pip install -r requirements.txt --break-system-packages
export DATABASE_URL="sqlite:///./test.db"
python -m uvicorn main:app --port 8000
```
(On Windows PowerShell: `$env:DATABASE_URL = "sqlite:///./test.db"`)

**Frontend:**
```bash
npm install
npm start
```

Open `http://localhost:3000`.

## Note
Answering is currently keyword-based FAQ matching against a seeded database — a deliberate first step prioritizing reliability and avoiding hallucination in a medical context, ahead of adding LLM-based generation.

## Built with
[my-agent-hub](https://github.com/rajaganaa/spec-driven-multi-ai-agents-) — an autonomous multi-agent coding system that plans, implements, tests, and reviews code from a plain-English goal.
