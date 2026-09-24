# CaseTree AI — Project Overview

**Full Name**: CaseTree AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching
**Version**: 0.0.1-SNAPSHOT (Scaffolded)
**Repository**: https://github.com/HoangNam2464/CaseTree-AI

---

## Problem Statement

University lecturers need engaging, pedagogically rich case studies that challenge students to make decisions under uncertainty and justify their reasoning. Creating these manually is time-consuming. CaseTree AI automates case generation from existing teaching materials while keeping the lecturer in control of what students receive.

---

## Core Value Proposition

1. **AI generates branching case studies** from the lecturer's own teaching materials (not generic content)
2. **Lecturer reviews and controls publication** — mandatory human-in-the-loop (DRAFT → REVIEWED → APPROVED → PUBLISHED)
3. **Supports dual learning modes**:
   - **Branching Study**: interactive decision tree navigation, choice consequences, student reasoning capture, and post-outcome reflection
   - **Review Study**: case data/context analysis, student proposed solutions, reasoning, lecturer feedback, and student reflection
4. **AI Reasoning / Challenge Support probes reasoning** — Socratic counter-questions (1-2 rounds, NO grading)
5. **Lecturer feedback & statistics** — qualitative commentary on student attempts/submissions, plus branch selection frequency and completion statistics

---

## Primary Actors

| Actor | Role |
|---|---|
| **Lecturer** | Creates courses, uploads materials, reviews/publishes cases, authors feedback on student work, inspects statistics |
| **Student** | Navigates Branching Case Player or Review Study, submits reasoning/solutions, engages in challenge support, reflects post-outcome/post-feedback |

---

## Core Workflow

### Branching Study Flow
```
1. Lecturer creates Course and uploads Teaching Materials (PDF / DOCX)
2. Materials processed: parsed → chunked → embedded → pgvector
3. Lecturer triggers AI Case Generation (Branching Study)
4. RAG retrieves relevant material → LLM generates decision tree (JSON)
5. Lecturer reviews, edits, approves, and publishes the case (PUBLISHED)
6. Student opens Branching Case Player, navigates nodes: Situation → Option selection → Student Reasoning submission → Consequence reveal
7. Optional AI Reasoning / Challenge Support (1-2 rounds of counter-questions, no grading)
8. Terminal outcome node reached → Student submits Post-Outcome Reflection
9. Lecturer inspects attempt path/reasoning and provides Lecturer Feedback
```

### Review Study Flow
```
1. Lecturer creates Review Study case with context_text and problem_text, then publishes
2. Student analyzes context, formulates proposed_solution and reasoning_text
3. Optional AI Reasoning / Challenge Support probes student solution/reasoning (1-2 rounds)
4. Student submits work (SUBMITTED)
5. Lecturer reviews submission and writes qualitative Lecturer Feedback (transitions to REVIEWED)
6. Student reviews lecturer feedback and submits Student Reflection (transitions to REFLECTED)
```

---

## Architecture Summary

| Layer | Technology | Role |
|---|---|---|
| Frontend | React 19 + Vite + TypeScript + TailwindCSS v4 + ReactFlow | Lecturer and Student UI |
| Backend Gateway | Node.js (NestJS 10 + TypeScript) | API Gateway, business state, persistence |
| AI Service | FastAPI (Python 3.12) + Pydantic v2 | Document parsing, RAG, case generation, debate (Internal) |
| Vector DB | PostgreSQL 16 + pgvector | Embeddings + relational business data |
| Cache & Session | Redis 7 | Caching, session store |
| Object Storage | MinIO | PDF/DOCX teaching material storage |
| LLM | Gemini 2.0 Flash / OpenAI GPT-4o-mini | Provider abstraction for text & embeddings |

---

## Documentation Index

| Category | Document | Description |
|---|---|---|
| **Audit & Requirements** | [Reference Repo Audit](architecture/REFERENCE-REPOSITORY-AUDIT.md) | Audit & classification of `ai-teacher-copilot` |
| | [Requirement Traceability](requirements/REQUIREMENT-TRACEABILITY.md) | 30 Proposal items mapped to documentation |
| **Architecture** | [Technology Stack ADR](architecture/ADR-001-TECHNOLOGY-STACK.md) | Technology choices & candidate options |
| | [System Architecture](architecture/SYSTEM-ARCHITECTURE.md) | Multi-tier overview & design principles |
| | [Service Boundaries](architecture/SERVICE-BOUNDARIES.md) | Inter-service contracts, protocols & security |
| | [System Data Flows](architecture/DATA-FLOW.md) | End-to-end sequence diagrams & lifecycle |
| | [Decision Tree Model](architecture/DECISION-TREE-MODEL.md) | Invariants & JSON schema for branching cases |
| | [Bootstrap Audit](architecture/BOOTSTRAP-AUDIT.md) | Comprehensive 11-section self-audit |
| **Features** | [Feature Specifications](features/) | 11 comprehensive 15-section specifications |
| **Data & AI** | [Data Model](database/DATA-MODEL.md) | PostgreSQL schema & SQL migration guide |
| | [RAG Pipeline](ai/RAG-PIPELINE.md) | Document parsing, chunking, retrieval & sources |
| | [Reasoning & Challenge Support](ai/REASONING-CHALLENGE-SUPPORT.md) | Counter-question rules, 2-round cap, non-grading mandate |
| **Research & QA** | [Testing Strategy](qa/TESTING-STRATEGY.md) | Test profiles, test boundaries & CI checks |
| | [Evaluation Design](research/EVALUATION-DESIGN.md) | Research questions, rubrics & dataset export |

---

## Feature Status Standard

All features are classified strictly under three states:
- **`Documented`**: Specification authored in `docs/` according to the 15-section standard.
- **`Structurally Scaffolded`**: Specification documented AND non-business architectural skeleton exists.
- **`Implemented`**: Complete business logic and workflow active (**Strictly ZERO in this task**).

| Feature Area | Status | Notes |
|---|---|---|
| Authentication & Roles | Structurally Scaffolded | JWT security, entity, and layout shell |
| Course Context | Structurally Scaffolded | Course entity, DTOs, and page shell |
| Teaching Materials & Upload | Structurally Scaffolded | Material metadata entity, MinIO config |
| Document Processing & RAG | Structurally Scaffolded | Parser/chunker shells, pgvector retrieval schema |
| AI Case Generation | Structurally Scaffolded | Pydantic schema, DFS validator, provider abstraction |
| Decision Tree Model | Structurally Scaffolded | Node, Option, Consequence domain models |
| Lecturer Review & Publishing | Structurally Scaffolded | ReactFlow canvas shell, status lifecycle |
| Branching Case Player & Attempts | Structurally Scaffolded | Attempt entity, node navigation shell, retry support |
| Student Reasoning Capture | Structurally Scaffolded | Reasoning entity, justification submission shell |
| Review Study Mode | Structurally Scaffolded | Submission entity, solution/reasoning forms |
| AI Reasoning / Challenge Support | Structurally Scaffolded | 2-round schema validator, challenge message model |
| Student Reflection | Structurally Scaffolded | Post-outcome / post-feedback reflection shell |
| Lecturer Feedback & Review | Structurally Scaffolded | Qualitative feedback entity, review dashboard |
| Lecturer Statistics | Structurally Scaffolded | Statistics aggregation query shells, page shell |
| Notifications | Documented | Proposal options (In-App / Email / Hybrid) |
| Quantitative Evaluation & Research | Documented | Rubric / export boundary (Implementation open) |

