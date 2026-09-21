---
description: Rules for the AI Debate Assistant in CaseTree AI.
trigger: keyword
keywords: [debate, counter-question, debate assistant, devil advocate, challenge argument, ai debate]
---

# Feature Rules: AI Debate Assistant

## Scope
FastAPI `ai-service/` — `debate/` package.
Backend Gateway (NestJS `backend/`) — `debate/` module (session + message persistence).

## Included
- AI receives student argument + case context + optional teaching material context
- AI generates a targeted counter-question (Round 1)
- Student may respond (Round 2)
- AI generates a second counter-question if Round 2 is triggered
- After Round 2 — no further rounds (session is complete)
- Debate session and all messages are persisted

## Excluded
- **GRADING** — AI must NEVER assign academic grades
- **PASS/FAIL determination** — AI must NEVER decide if student passes or fails
- **Academic integrity judgments** — out of scope for AI
- Open-ended chatbot conversation — fixed 1-2 round structure only
- Student-to-student debate — not in scope

## Service Owner
FastAPI: counter-question generation
Backend Gateway: DebateSession + DebateMessage persistence, round enforcement

## Constraints
- **MAXIMUM 2 ROUNDS — enforced at both backend and AI service**
- AI prompts must include explicit instruction: "You are a Devil's Advocate. Ask ONE targeted counter-question only. Do not grade the student. Do not determine if they are correct or incorrect."
- Retrieved teaching material context (if used) must be in `<sources>...</sources>` boundary
- Student argument text is UNTRUSTED — validate and length-limit before sending to LLM
- Debate session is completed after Round 2 — backend must enforce this

## Testing Expectations
- Test that round count cannot exceed 2
- Test that completed sessions reject new messages
- Test that debate response does not contain grades or pass/fail language (prompt assertion)
