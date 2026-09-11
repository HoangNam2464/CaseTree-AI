# EduBranch AI — Project Overview

**Full Name**: EduBranch AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching
**Version**: 0.0.1-SNAPSHOT (Scaffolded)
**Repository**: https://github.com/HoangNam2464/EduBranch-AI

---

## Problem Statement

University lecturers need engaging, pedagogically rich case studies that challenge students to make decisions under uncertainty and justify their reasoning. Creating these manually is time-consuming. EduBranch AI automates case generation from existing teaching materials while keeping the lecturer in control of what students receive.

---

## Core Value Proposition

1. **AI generates branching case studies** from the lecturer's own teaching materials (not generic content)
2. **Lecturer reviews and controls publication** — mandatory human-in-the-loop
3. **Students engage interactively** — not passive reading, but active decision-making
4. **AI Debate Assistant challenges reasoning** — Socratic counter-questioning (not grading)
5. **Lecturer can inspect outcomes** — simple statistics on branch choices and arguments

---

## Primary Actors

| Actor | Role |
|---|---|
| **Lecturer** | Creates courses, uploads materials, reviews/publishes cases, inspects statistics |
| **Student** | Navigates simulator, makes decisions, writes arguments, engages in debate |

---

## Core Workflow

```
1. Lecturer creates a Course
2. Lecturer uploads Teaching Materials (PDF / DOCX)
3. Materials are processed: parsed → chunked → embedded → pgvector
4. Lecturer triggers AI Case Generation
5. RAG retrieves relevant material → LLM generates branching case (JSON)
6. Case created as DRAFT
7. Lecturer reviews, edits, approves the case
8. Lecturer publishes the case (PUBLISHED)
9. Student opens the Case Simulator
10. Student navigates the decision tree (Situation → Option → Consequence → Next Node)
11. Student writes a justification/argument
12. AI Debate Assistant asks 1 counter-question
13. Student may respond (Round 2)
14. Debate ends — session completed
15. Lecturer reviews branch patterns and student arguments
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
| **Data & AI** | [Data Model](database/DATA-MODEL.md) | PostgreSQL schema & Flyway migration guide |
| | [RAG Pipeline](ai/RAG-PIPELINE.md) | Document parsing, chunking, retrieval & sources |
| | [Debate Assistant](ai/DEBATE-ASSISTANT.md) | Devil's advocate rules & 2-round cap |
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
| AI Case Generation | Structurally Scaffolded | Pydantic schema, BFS validator, provider abstraction |
| Decision Tree Model | Structurally Scaffolded | Node, Option, Consequence domain models |
| Lecturer Review & Publishing | Structurally Scaffolded | ReactFlow canvas shell, status lifecycle |
| Student Simulator | Structurally Scaffolded | Simulation session model, node navigation shell |
| Student Argument Capture | Structurally Scaffolded | Argument model, justification submission shell |
| AI Debate Assistant | Structurally Scaffolded | 2-round schema validator, debate message model |
| Lecturer Statistics | Structurally Scaffolded | Statistics aggregation query shells, page shell |
| Notifications | Documented | Proposal options (In-App / Email / Hybrid) |
| Quantitative Evaluation & Research | Documented | Rubric / export boundary (Implementation open) |

