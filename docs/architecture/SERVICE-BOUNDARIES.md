# CaseTree AI — Service Boundaries & Contracts

> **Document Status**: Authoritative Architecture Specification  
> **Target Audience**: Backend Engineers, AI Engineers, Frontend Engineers  
> **Core Architecture Mandate**: `Frontend (Browser) → Backend Gateway → AI Service (Internal Only)`. Direct communication from the Frontend to the AI Service is strictly prohibited.

---

## 1. System Boundary Overview

```
┌────────────────────────────────────────────────────────┐
│  Client Tier (Browser)                                 │
│  React 19 + Vite + TypeScript + TailwindCSS v4 + Flow  │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / REST API + JWT
                            ▼
┌────────────────────────────────────────────────────────┐
│  Backend Gateway (Node.js NestJS 10 + TypeScript)      │
│  • Auth, Users, Roles (LECTURER, STUDENT)              │
│  • Course Context & Material Metadata                  │
│  • Case Lifecycle & State Machine                      │
│  • Simulation Sessions & Student Arguments             │
│  • Debate History Persistence & Round Enforcement      │
│  • Lecturer Statistics & Evaluation Extension          │
└────────────┬──────────────┬──────────────────┬─────────┘
             │              │                  │ Internal HTTP
             │ SQL / Schema │ S3 API           │ + X-Internal-API-Key
             ▼              ▼                  ▼
┌──────────────────┐ ┌─────────────┐ ┌───────────────────────────┐
│ PostgreSQL 16    │ │ MinIO S3    │ │ FastAPI AI Service        │
│ + pgvector       │ │ (PDF/DOCX)  │ │ (INTERNAL ONLY)           │
│ (Metadata & DB)  │ └─────────────┘ │ • Document Parser/Chunker │
└──────────────────┘                 │ • pgvector Semantic Search│
┌──────────────────┐                 │ • Structured LLM Case Gen │
│ Redis 7 (Cache)  │                 │ • AI Debate Assistant     │
└──────────────────┘                 └─────────────┬─────────────┘
                                                   │ HTTPS
                                                   ▼
                                     ┌───────────────────────────┐
                                     │ LLM Providers             │
                                     │ Gemini 2.0 / GPT-4o-mini  │
                                     └───────────────────────────┘
```

---

## 2. Service Ownership & Responsibility Matrix

| Concern / Responsibility | Frontend | Backend Gateway | FastAPI AI Service | PostgreSQL / MinIO |
| :--- | :---: | :---: | :---: | :---: |
| **User Authentication & JWT Issuance** | ❌ (View only) | ✅ **Sole Owner** | ❌ Forbidden | Database (`users`) |
| **Role Authorization (Lecturer vs. Student)** | ❌ (Client guard) | ✅ **Sole Owner** | ❌ Forbidden | Database (`users.role`) |
| **Course & Material Metadata Management** | ❌ | ✅ **Sole Owner** | ❌ Forbidden | Database (`courses`, `materials`) |
| **Binary File Upload & Storage** | Form upload | ✅ Verifies & Streams | ❌ Forbidden | MinIO (`casetree-materials`) |
| **Document Text Parsing (PDF/DOCX)** | ❌ | ❌ Delegated | ✅ **Sole Owner** | Streams from MinIO |
| **Document Chunking & Token Splitting** | ❌ | ❌ Delegated | ✅ **Sole Owner** | Memory |
| **Vector Embedding Generation** | ❌ | ❌ Delegated | ✅ **Sole Owner** | Provider API |
| **Vector Indexing & Similarity Retrieval** | ❌ | ❌ Delegated | ✅ **Sole Owner** | PostgreSQL (`document_chunks`) |
| **Decision Tree Generation Prompting** | ❌ | ❌ Delegated | ✅ **Sole Owner** | Provider API |
| **Decision Tree Schema & Cycle Validation**| ❌ | ✅ Double-checks | ✅ **Sole Owner** | Memory (Pydantic / BFS) |
| **Case Lifecycle (DRAFT → PUBLISHED)** | ❌ | ✅ **Sole Owner** | ❌ Forbidden | Database (`cases.status`) |
| **Interactive Tree Rendering (ReactFlow)** | ✅ **Sole Owner** | ❌ (Supplies JSON) | ❌ Forbidden | Client DOM |
| **Simulation Session & State Navigation** | ❌ (Renders node)| ✅ **Sole Owner** | ❌ Forbidden | Database (`simulation_sessions`)|
| **Student Argument Persistence** | Form submit | ✅ **Sole Owner** | ❌ Forbidden | Database (`student_arguments`) |
| **AI Debate Prompting & Counter-Questions**| ❌ | ❌ Calls AI service| ✅ **Sole Owner** | Provider API |
| **Debate Max 2 Rounds Enforcement** | UI disable | ✅ **Hard Enforcer** | ✅ **Schema Gate** | Database (`debate_sessions`) |
| **Lecturer Branch & Choice Statistics** | Visual charts | ✅ **Sole Owner** | ❌ Forbidden | Database Aggregations |
| **Research Dataset Export** | ❌ | ✅ **Sole Owner** | ❌ Forbidden | Anonymized CSV/JSON |

---

## 3. Communication Protocols & Security Contracts

### 3.1 Frontend ↔ Backend Gateway Contract
- **Protocol**: HTTPS / REST.
- **Authentication**: Bearer JWT token in `Authorization: Bearer <token>` header.
- **Payload Format**: `application/json` wrapped in standardized response structure:
  ```json
  {
    "success": true,
    "data": { ... },
    "error": null,
    "timestamp": "2026-09-11T12:00:00Z"
  }
  ```
- **Security Rule**: The frontend client must **never** receive internal IDs, database connection strings, or internal service API keys.

### 3.2 Backend Gateway ↔ FastAPI AI Service Contract
- **Protocol**: HTTP/1.1 (within internal container network, e.g. `http://ai-service:8000`).
- **Network Scope**: Strictly internal. The AI service port must **never** be exposed to public ingress or reverse proxies.
- **Authentication**: Header-based shared secret: `X-Internal-API-Key: <secret>`.
- **Payload Format**: Strict JSON models validated by Pydantic v2.
- **Error Propagation**: Standard HTTP status codes (400 for schema validation failures, 422 for unprocessable entities, 502 for upstream LLM provider failures).

### 3.3 AI Service ↔ LLM Provider Contract
- **Protocol**: HTTPS outbound via official SDK or REST client.
- **Authentication**: API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`) loaded via environment variables.
- **Untrusted Content Boundary**: All text retrieved from teaching materials MUST be injected inside explicit XML-like boundaries:
  ```
  <sources>
  [Retrieved Document Chunks]
  </sources>
  ```
  System instructions must explicitly instruct the LLM that content within `<sources>` is unverified reference data and cannot override system instructions or persona constraints.

---

## 4. Architectural Invariants

1. **Publication Gate**: A Student user can **never** access a case that is not in `PUBLISHED` status. This constraint is enforced at the database repository query level (e.g. `WHERE status = 'PUBLISHED'`), not just in UI controllers.
2. **AI Independence from Grading**: The AI Debate Assistant has zero grading logic, zero scoring rubrics, and zero pass/fail endpoints.
3. **Round Cap**: The AI Debate Assistant is hard-capped at 2 rounds of counter-questioning. The Backend Gateway rejects any debate request where `current_round >= 2`.
