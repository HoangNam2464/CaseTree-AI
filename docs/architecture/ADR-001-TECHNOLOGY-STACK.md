# ADR-001: Technology Stack Selection & Candidate Options

> **Status**: Candidate Options Documented (Backend pending Project Owner confirmation)  
> **Date**: 2026-09-11  
> **Classification Standard**: Every decision item is tagged with:
> - `[A. Proposal Requirement]`: Explicitly stated in the Edu-Branch-AI Proposal (C1SE.65).
> - `[B. Project-Owner Decision]`: Explicitly confirmed by the project owner.
> - `[C. Reference Repository Pattern]`: Pattern observed in `ai-teacher-copilot`.
> - `[D. Architectural Decision]`: System-level architectural design choice.
> - `[E. Candidate Option / Project Owner Decision Required]`: Unresolved choice requiring owner sign-off.

---

## 1. Context

Edu-Branch-AI is an interactive branching case study platform for university education. The authoritative Proposal permits various technology alternatives, while the initial scaffolding inherited specific choices from the engineering reference repository (`ai-teacher-copilot`). 

This ADR establishes the current baseline, clearly distinguishing confirmed decisions from candidate options.

---

## 2. Technology Classification & Decision Matrix

### 2.1 Backend Gateway Framework
- **Status**: `[A. Proposal Requirement]` & `[B. Project Owner Ratified Decision]`
- **Proposal Baseline**: Section 7 (p. 11) and Section 11 (p. 16) explicitly specify: *"Backend: Node.js (NestJS/Express) or Python FastAPI"*.
- **Selected Baseline**: **Node.js (NestJS 10 + TypeScript)**
- **Rationale**:
  1. Aligns directly with Proposal Section 7 & 11 (`Node.js (NestJS/Express)`).
  2. Shares the TypeScript ecosystem with the React frontend for shared DTOs and type safety.
  3. Enterprise modular architecture (Modules, Controllers, Services, Guards) directly models Edu-Branch-AI's 11 domain feature areas.
  4. Inherited Spring Boot 3 (Java 17) scaffold from `ai-teacher-copilot` has been cleanly removed and replaced.

---

### 2.2 AI Service Framework
- **Status**: `[D. Architectural Decision]` & `[B. Project-Owner Decision]`
- **Selection**: **Python 3.12 + FastAPI** (Internal Service Only)
- **Rationale**:
  - Python is the primary ecosystem for AI/LLM libraries, document parsers (PyPDF, python-docx), and vector store connectors (asyncpg, pgvector).
  - FastAPI provides high-performance asynchronous request handling and native integration with Pydantic v2 for strict schema validation.
  - The Project Owner confirmed a separate, internal AI service.

---

### 2.3 Frontend Framework & Styling
- **Status**: `[A. Proposal Requirement]` & `[D. Architectural Decision]`
- **Selection**: **React 19 + Vite + TypeScript + TailwindCSS v4**
- **Rationale**:
  - The Proposal permits *React.js / Next.js* and explicitly specifies **TailwindCSS** (Section 11, p. 16).
  - Vite provides rapid build and hot-module reload times for development.
  - TailwindCSS v4 provides streamlined modern CSS engine with zero runtime overhead.
  - TypeScript provides compile-time type safety across complex decision-tree states.

---

### 2.4 Decision Tree Visualization
- **Status**: `[A. Proposal Requirement]`
- **Selection**: **ReactFlow**
- **Rationale**:
  - The Proposal explicitly lists *"Visual/graph library: ReactFlow or jsPlumb (for case-tree display)"* (Section 11, p. 16).
  - ReactFlow is actively maintained, highly optimized for React DOM rendering, and provides built-in node/edge customizability for the Case Review form editor and Simulator navigator.

---

### 2.5 Relational Database & Vector Store
- **Status**: `[A. Proposal Requirement]` & `[B. Project-Owner Decision]`
- **Selection**: **PostgreSQL 16 + pgvector extension**
- **Rationale**:
  - The Proposal lists PostgreSQL as the primary database option (Section 11, p. 16).
  - The Project Owner explicitly confirmed PostgreSQL with `pgvector` to unify business relational data and semantic embedding vectors in a single robust ACID database engine, avoiding the operational overhead of a separate vector database (e.g. Pinecone/Qdrant).

---

### 2.6 Cache & Session Store
- **Status**: `[A. Proposal Requirement]` & `[B. Project-Owner Decision]`
- **Selection**: **Redis 7**
- **Rationale**:
  - Explicitly specified in the Proposal: *"Database & cache: PostgreSQL (or MongoDB), Redis"* (Section 11, p. 16).
  - Confirmed by Project Owner for fast token blacklist checking, session management, and rate limiting.

---

### 2.7 Object Storage
- **Status**: `[B. Project-Owner Decision]`
- **Selection**: **MinIO** (S3-compatible)
- **Rationale**:
  - The Project Owner explicitly decided on MinIO for storing teaching material documents (PDF/DOCX).
  - S3 API compatibility allows seamless local development in Docker and frictionless future migration to AWS S3 or Google Cloud Storage in production without changing application code.

---

### 2.8 LLM Providers & Provider Abstraction
- **Status**: `[A. Proposal Requirement]` & `[D. Architectural Decision]`
- **Selection**: **Google Gemini 2.0 Flash / OpenAI GPT-4o-mini via Provider Abstraction (`providers/factory.py`)**
- **Rationale**:
  - The Proposal explicitly identifies low-cost, fast models: *"AI/LLM: OpenAI GPT-4o-mini / Gemini Flash API"* (Section 6, p. 10 & Section 11, p. 16).
  - A provider abstraction layer decouples route handlers from vendor-specific SDK changes, allowing runtime switching via `AI_PROVIDER=gemini` or `AI_PROVIDER=openai`.

---

### 2.9 RAG Orchestration Technology
- **Status**: `[A. Proposal Requirement]` (Allowed / Possible Option)
- **Selection**: **LangChain** (Allowed/Possible Option)
- **Rationale**:
  - The Proposal mentions LangChain under tools: *"OpenAI GPT-4o-mini / Gemini Flash API + LangChain (for RAG orchestration and structured output)"* (Section 11, p. 16).
  - LangChain is documented as an allowed and supported option for text chunking, prompt template management, and retrieval orchestration, but is not a rigid mandatory architectural constraint. Pure Python or lightweight orchestrations are permitted if required.

---

## 3. Service Boundary Architecture

```
Client (Browser — React 19 + TailwindCSS v4)
    │
    ▼ [REST API + JWT]
Backend Gateway [Node.js (NestJS 10 + TypeScript)]
    │
    ├─────────► PostgreSQL 16 + pgvector (Business metadata)
    ├─────────► MinIO (PDF / DOCX files)
    ├─────────► Redis 7 (Cache / Sessions)
    │
    ▼ [Internal HTTP + X-Internal-API-Key]
AI Service (Python FastAPI — Internal Only)
    │
    ├─────────► PostgreSQL 16 + pgvector (Vector search)
    │
    ▼ [HTTPS API]
LLM Providers (Gemini 2.0 Flash / OpenAI GPT-4o-mini)
```

---

## 4. Consequences & Action Items

1. Backend Gateway is formally established as **Node.js (NestJS 10 + TypeScript)**, fully compliant with Proposal Sections 7 & 11.
2. Frontend baseline is formally established as **React 19 + TailwindCSS v4**.
3. All inherited Spring Boot 3 / Java / Maven artifacts have been removed.
4. All 14 `.agents/rules/` files have been harmonized with the ratified technology baseline.
5. All business features remain **unimplemented** (structural skeleton only).
