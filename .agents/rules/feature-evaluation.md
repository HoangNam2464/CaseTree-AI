---
description: Rules for the research evaluation boundary in Edu-Branch-AI.
trigger: keyword
keywords: [evaluation, research, rubric, survey, dataset, export]
---

# Feature Rules: Evaluation / Research Boundary

## Scope
Backend Gateway (NestJS `backend/`) — `evaluation/` module.
FastAPI `ai-service/` — `evaluation/` package.

## Included (Scaffolded only in MVP)
- Rubric definition and storage
- Evaluation record (lecturer manually links rubric to a session)
- Survey/data collection placeholder
- Research dataset export (anonymized)
- AI-generated vs lecturer-authored case comparison placeholder

## Excluded
- Full research experiment implementation — not in MVP
- Automated AI-based evaluation — not in MVP scope
- Public dataset publishing — not in MVP

## Service Owner
Backend Gateway: rubric and evaluation record persistence
FastAPI: AI-specific evaluation metric utilities (scaffolded)

## Constraints
- Research dataset exports MUST be anonymized (no PII)
- This is a foundation/boundary only — do not build the full research system in MVP

## Testing Expectations
- Minimal placeholder tests — full suite in a later phase
