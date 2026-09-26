# Edu-Branch-AI — Project Overview

**Full Name**: Edu-Branch-AI — AI Platform for Experiential Case-Based Learning in University Teaching
**Version**: 0.0.1-SNAPSHOT (Scaffolded)
**Repository**: https://github.com/HoangNam2464/EduBranch-AI

---

## Problem Statement

University lecturers need engaging, pedagogically rich case studies that challenge students to make decisions under real-world uncertainty. Creating these manually is time-consuming and hard to scale. Edu-Branch-AI automates case generation from existing teaching materials while keeping the lecturer in full control of what students receive and experience.

Students learn not by passively reading outcomes, but by making decisions, completing the full journey, then reviewing *how* each of their choices shaped the result — connecting personal experience to course material.

---

## Core Value Proposition

1. **AI generates case studies from the lecturer's own materials** — not generic content. Both Branching Study (interactive decision journeys) and Review Study (open analysis) cases are grounded in the actual syllabus, teaching materials, and course data uploaded by the lecturer.
2. **Lecturer reviews and controls publication** — mandatory human-in-the-loop (DRAFT → REVIEWED → APPROVED → PUBLISHED). No case reaches students without explicit lecturer approval.
3. **Supports dual learning modes**:
   - **Branching Study**: students experience a situational journey through consecutive decisions (no interruptions mid-flow), then enter a structured REVIEW phase to look back at every choice, understand its effect on the outcome, write retrospective reasoning, reflect, and optionally retry with a new attempt.
   - **Review Study**: students analyze case context and data, propose a solution with reasoning, receive qualitative lecturer feedback, and complete a reflection. No decision tree required.
4. **AI Reasoning / Challenge Support probes reasoning** — Socratic counter-questions (1–2 rounds, NO grading, NO scoring, NO pass/fail).
5. **Lecturer feedback & statistics** — qualitative commentary on student attempts/submissions, plus branch selection frequency and completion statistics for classroom discussion.

---

## Primary Actors

| Actor | Role |
|---|---|
| **Lecturer** | Creates courses; uploads teaching materials; triggers AI case generation; inspects, edits, approves, and publishes cases; shares case link with students; reviews student attempts/submissions; writes qualitative feedback; uses statistics for class discussion. |
| **Student** | Accesses case via direct link from lecturer. In Branching Study: navigates the experience, makes consecutive decisions, completes the journey, reviews the full path retrospectively, writes reasoning and reflection, and may retry. In Review Study: analyzes context, proposes solution, receives feedback, reflects. |

> **Students do not create cases.** Students do not browse case lists. Student access is always via a direct link provided by the Lecturer.

---

## Core Workflow

### Lecturer → Case → Student Flow
```
1. Lecturer creates Course and uploads Teaching Materials (PDF / DOCX)
2. Materials processed: parsed → chunked → embedded → pgvector
3. Lecturer triggers AI Case Generation (Branching Study or Review Study)
4. RAG retrieves relevant material → LLM generates structured case draft
5. Lecturer inspects, edits nodes/options/consequences/questions, approves, and publishes
6. Lecturer sends the published case link to students (e.g. via LMS, email, or in-class)
7. Students open the link and begin the learning experience
```

### Branching Study Flow (Student)

**Phase 1 — Experience (No interruptions mid-flow)**
```
Initial Situation + Context / Data presented
            ↓
Decision Point → Student selects an option
            ↓
Next Situation (seamless — no consequence card, no reasoning form between nodes)
            ↓
Decision Point → Student selects next option
            ↓
... (variable number of decision points depending on case structure)
            ↓
Terminal Node → Journey complete
```

**Phase 2 — REVIEW (Retrospective — after journey is complete)**
```
Full journey replay shown to student:
  • Every decision point traversed, in order
  • The option chosen at each point
  • The path taken and what the alternatives were
  • How each choice contributed to the outcome
  • Which decisions were pivotal to the final result
            ↓
Student writes reasoning for key decisions (retrospective, not per-click)
Student can see: "Why this choice? What would have changed if I chose differently?"
```

**Phase 3 — Reflection & Retry**
```
Student submits overall Reflection
            ↓
[Optional: AI Reasoning / Challenge Support — max 2 rounds, counter-questions only, no grading]
            ↓
[Optional: Retry → New Attempt → Student explores a different path from scratch]
```

### Review Study Flow (Student)
```
1. Student opens case: reads context_text (situation + background data)
2. Student reads problem_text (the open question/problem to analyze)
3. Student writes analysis and proposes a solution with reasoning (student_analysis, proposed_solution, reasoning_text)
4. [Optional] AI Reasoning / Challenge Support: counter-questions to probe student's reasoning (max 2 rounds)
5. Student submits work → Status: SUBMITTED
6. Lecturer reviews submission, writes qualitative feedback → Status: REVIEWED
7. Student reads feedback, writes reflection → Status: REFLECTED
```

---

## Architecture Summary

| Layer | Technology | Role |
|---|---|---|
| Frontend | React 19 + Vite + TypeScript + TailwindCSS v4 + ReactFlow | Lecturer and Student UI |
| Backend Gateway | Node.js (NestJS 10 + TypeScript) | API Gateway, business state, persistence |
| AI Service | FastAPI (Python 3.12) + Pydantic v2 | Document parsing, RAG, case generation, challenge support (Internal) |
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
| **Features** | [Feature Specifications](features/) | Comprehensive per-feature specifications |
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
- **`Implemented`**: Complete business logic and workflow active (**Strictly ZERO in this snapshot**).

| Feature Area | Status | Notes |
|---|---|---|
| Authentication & Roles | Structurally Scaffolded | JWT security, entity, and layout shell |
| Course Context | Structurally Scaffolded | Course entity, DTOs, and page shell |
| Teaching Materials & Upload | Structurally Scaffolded | Material metadata entity, MinIO config |
| Document Processing & RAG | Structurally Scaffolded | Parser/chunker shells, pgvector retrieval schema |
| AI Case Generation | Structurally Scaffolded | Pydantic schema, DFS validator, provider abstraction |
| Decision Tree Model | Structurally Scaffolded | Node, Option, Consequence domain models |
| Lecturer Review & Publishing | Structurally Scaffolded | ReactFlow canvas shell, status lifecycle |
| Branching Case Player & Attempts | Structurally Scaffolded | Attempt entity, node navigation shell, seamless experience flow |
| Student Reasoning Capture (REVIEW phase) | Structurally Scaffolded | Reasoning entity — captured retrospectively after journey completion |
| Review Study Mode | Structurally Scaffolded | Submission entity, solution/reasoning forms |
| AI Reasoning / Challenge Support | Structurally Scaffolded | 2-round schema validator, challenge message model |
| Student Reflection | Structurally Scaffolded | Post-journey / post-feedback reflection shell |
| Lecturer Feedback & Review | Structurally Scaffolded | Qualitative feedback entity, review dashboard |
| Lecturer Statistics | Structurally Scaffolded | Statistics aggregation query shells, page shell |
| Notifications | Documented | Proposal options (In-App / Email / Hybrid) |
| Quantitative Evaluation & Research | Documented | Rubric / export boundary (Implementation open) |
