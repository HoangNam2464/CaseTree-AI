---
description: Rules for AI case generation in Edu-Branch-AI.
trigger: keyword
keywords: [case generation, ai generate, decision tree generation, rag, case generator, structured output]
---

# Feature Rules: AI Case Generator

## Scope
FastAPI `ai-service/` — `generation/` package.
Backend Gateway (NestJS `backend/`) — `case/` module (receives and persists generated case).

## Included
- Lecturer triggers case generation from teaching materials
- Backend Gateway calls FastAPI with material IDs and optional topic hint
- FastAPI performs RAG retrieval → prompt construction → LLM call → structured output
- Generated output validated against CaseGenerationOutput Pydantic schema
- Decision tree structure validated (no orphans, no cycles, at least one terminal node)
- Backend Gateway receives validated case and persists as CaseStatus.DRAFT
- Case starts as DRAFT — lecturer must review before publication

## Excluded
- Automatic publishing without lecturer review — out of scope
- Multi-step retrieval or reranking — basic top-K retrieval in MVP
- Fine-tuning — out of scope

## Service Owner
FastAPI: RAG, prompt, LLM, schema validation
Backend Gateway: persistence, lifecycle management

## Constraints
- Retrieved chunks MUST be enclosed in `<sources>...</sources>` boundary
- Source content must NOT override system instructions
- Generated case must validate against CaseGenerationOutput schema before returning
- No cycle in decision tree (enforced by BFS validation)
- At least 2 nodes and 1 terminal node
- Cite source_chunk_ids for provenance/citation support

## Prompt Security
- System prompt defines the task and output format
- Retrieved teaching material goes ONLY into the `<sources>...</sources>` section
- Never concatenate source content directly into the system prompt

## Testing Expectations
- Pydantic schema validation test (valid and invalid trees)
- Cycle detection test
- Orphan node detection test
- Terminal node requirement test
