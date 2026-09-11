# EduBranch AI — AI Coding Agent Instructions

> **Document Status**: Authoritative Agent Governance Instructions  
> **Target Audience**: GitHub Copilot, Antigravity, Claude, and all AI coding assistants operating on this repository.

---

## 1. The 12 Cardinal Rules for AI Coding Agents

Every AI agent working on EduBranch AI MUST strictly adhere to the following 12 rules:

1. **Read Project Foundation Rules First**: Always read `.agents/rules/00-project-foundation.md` before analyzing, planning, or modifying any code.
2. **Read Applicable Feature Rules Before Changing a Feature**: Consult the corresponding rule in `.agents/rules/feature-*.md` and specification in `docs/features/FEATURE-*.md` before proposing or touching code in that feature area.
3. **Follow the Proposal**: The authoritative product definition is the EduBranch AI Proposal (`C1SE_65-EduBranch-AI-Proposal_V1.0.docx`). Never invent features not grounded in this document.
4. **Follow Applicable Markdown Rules**: Project governance is defined in Markdown rules. They are mandatory constraints, not optional suggestions.
5. **Never Invent Scope**: Keep strictly to university branching case studies and debate. Exclude lesson planners, quiz generators, LMS integrations, social login, and unrelated features.
6. **Never Copy AI Teacher Copilot Business Logic**: The reference repository (`ai-teacher-copilot`) is an engineering reference only. Do NOT copy its source code, K-12 domain models, or teacher workspace features.
7. **Respect Service Boundaries**: The client tier communicates exclusively with the Backend Gateway. The FastAPI AI Service is **internal only** and must never be exposed to the public internet or called directly from the frontend.
8. **Protect Secrets**: Never hardcode, commit, or expose API keys, JWT secrets, database credentials, or internal tokens. Always use environment variables loaded from `.env` (which is excluded from Git).
9. **Validate Changes**: Validate syntax, types, and constraints before completing tasks. Never create dummy code or fake implementations to bypass tests.
10. **Document Architectural Decisions**: Document all significant design choices in `docs/architecture/` using Architecture Decision Records (ADRs).
11. **Keep Changes Scoped**: Keep branches and pull requests tightly focused on a single feature or fix (`type(scope): description`). Do not perform sweeping unsolicited refactors.
12. **Ask Before Acting on Ambiguity**: If any requirement, architectural choice, Markdown rule, or existing code remains ambiguous, **STOP and ask the Project Owner**. Never guess or assume.

---

## 2. Project Identity & Purpose

- **Name**: EduBranch AI (NOT "AI Teacher Copilot").
- **Full Title**: EduBranch AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching.
- **Target Audience**: University lecturers and undergraduate/graduate students (NOT K-12).
- **Core Loop**: Teaching Material → RAG Processing → AI-Generated Branching Case Study → Lecturer Review/Edit → Lecturer Approval & Publication → Student Simulation → Immediate Consequence & Argument Justification → AI Debate Assistant (Devil's Advocate, 1–2 rounds max, no grading) → Lecturer Statistics.

---

## 3. Confirmed Architecture & Service Ownership

```
Frontend (Browser) ──[HTTPS + JWT]──► Backend Gateway ──[Internal HTTP + Token]──► FastAPI AI Service ──► LLM
```

| Concern / Responsibility | Backend Gateway | FastAPI AI Service (Internal) |
| :--- | :---: | :---: |
| Authentication & JWT Issuance | ✅ | ❌ |
| User & Role Management (Lecturer / Student) | ✅ | ❌ |
| Course & Material Metadata | ✅ | ❌ |
| Case Lifecycle State Machine | ✅ | ❌ |
| Simulation Session Persistence | ✅ | ❌ |
| Student Argument Persistence | ✅ | ❌ |
| Debate History Persistence | ✅ | ❌ |
| Lecturer Statistics Aggregations | ✅ | ❌ |
| Document Parsing (PDF/DOCX) | ❌ | ✅ |
| Token Chunking & Embeddings | ❌ | ✅ |
| pgvector Semantic Retrieval | ❌ | ✅ |
| RAG Prompt Assembly & Sources Boundary | ❌ | ✅ |
| Structured Decision Tree Generation (LLM) | ❌ | ✅ |
| AI Debate Counter-Question Prompting | ❌ | ✅ |

---

## 4. Decision-Tree Integrity & AI Governance Rules

- **Untrusted Document Content**: All retrieved chunks from teaching materials MUST be encapsulated in `<sources>...</sources>` tags to prevent indirect prompt injection.
- **Human-in-the-Loop**: AI-generated cases are ALWAYS born in `DRAFT` status. Students must NEVER receive or access cases that are not in `PUBLISHED` status.
- **AI Never Grades**: The AI Debate Assistant acts strictly as a **Socratic Devil's Advocate**. It must never assign grades, letter scores, numerical ratings, pass/fail decisions, or academic integrity judgments.
- **Debate Round Cap**: The Debate Assistant is hard-capped at **2 rounds maximum**. Enforced at both backend and AI service layers.
- **Graph Invariants**: Every decision tree must be a directed acyclic graph (no loops, no cycles, no orphan nodes, reachable from root, at least one terminal node).
