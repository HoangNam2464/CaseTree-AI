# EduBranch AI — FastAPI AI Service

Internal-only AI service for the EduBranch AI platform.

> ⚠️ This service is INTERNAL ONLY. It must not be exposed to the internet.
> All requests must include the `X-Internal-API-Key` header.

## Responsibilities

- Document parsing (PDF, DOCX via PyPDF + python-docx)
- Document chunking (via LangChain text splitters)
- Embedding generation (via OpenAI or Gemini)
- pgvector semantic retrieval
- RAG orchestration
- Case generation with structured JSON output (validated by Pydantic)
- AI Debate Assistant (targeted counter-questions, max 2 rounds)
- AI evaluation utilities

## Technology

- **Runtime**: Python 3.12
- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **RAG**: LangChain (text splitters, retrieval)
- **LLM**: OpenAI GPT-4o-mini / Google Gemini Flash (provider abstraction)
- **Vector DB**: pgvector via asyncpg
- **Logging**: structlog

## Domain Structure

```
app/
├── core/          ← Config, security, logging, exceptions
├── providers/     ← LLM provider abstraction (base, openai, gemini, factory)
├── ingestion/     ← Document parser + chunker
├── retrieval/     ← Embedding + pgvector retrieval
├── generation/    ← Case generator + decision tree schemas
├── debate/        ← AI Debate Assistant + schemas
└── evaluation/    ← AI evaluation utilities
```

## Local Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Fill in API keys and database credentials

# 4. Start the service
uvicorn app.main:app --reload --port 8000

# Health check (no auth required)
curl http://localhost:8000/health
```

## Testing

```bash
pytest
```

## Security Rules

- Never write vendor-specific LLM SDK code in route handlers
- Always use `app.providers.factory.get_provider()` for LLM access
- Always wrap retrieved document chunks in `<sources>...</sources>` boundary
- Never pass raw user/document content directly to system prompts
- The Debate Assistant MUST NOT grade students or make pass/fail decisions
