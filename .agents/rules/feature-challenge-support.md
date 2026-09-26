---
description: Rules for AI Reasoning / Challenge Support in Edu-Branch-AI.
trigger: keyword
keywords: [challenge support, counter-question, ai reasoning, challenge question, reasoning support]
---

# Feature Rules: AI Reasoning / Challenge Support

## Scope
FastAPI `ai-service/` — `challenge_support/` package.
Backend Gateway (NestJS `backend/`) — `challenge-support/` module (session + message persistence).
Frontend — `pages/student/ChallengeSupportPage.tsx`.

## Included
- Supports **both** learning modes: probes `student_reasoning` (Branching Study) or `proposed_solution`/`reasoning_text` in `review_study_submissions` (Review Study)
- AI receives the student's reasoning + case context + relevant teaching-material chunks (wrapped in `<sources>...</sources>`)
- AI generates ONE targeted, contextual challenge/counter-question (Round 1) probing assumptions and trade-offs
- Student may optionally respond/clarify (Round 2)
- AI generates one final follow-up question if Round 2 is triggered
- After Round 2 — no further rounds; session is marked `is_completed = TRUE`
- Session and all messages are persisted (`challenge_support_sessions`, `challenge_messages`)
- Exactly one target per session: `reasoning_id` XOR `review_submission_id` (`chk_challenge_one_target`)

## Excluded
- **GRADING** — AI must NEVER assign academic grades, scores, or numerical ratings
- **PASS/FAIL determination** — AI must NEVER decide if a student is correct or incorrect
- **Academic integrity judgments** — out of scope for AI
- Open-ended chatbot conversation — fixed 1–2 round structure only, hard-capped
- Student-to-student debate — not in scope
- **Debate platform framing** — this is a support function embedded in the student's learning flow, not a standalone debate mode or independent platform

## Service Owner
FastAPI: counter-question generation (`challenge_support/`).
Backend Gateway: `challenge_support_sessions` + `challenge_messages` persistence, round enforcement.

## Constraints
- **MAXIMUM 2 ROUNDS — enforced at both backend and AI service** (`CHECK (current_round >= 0 AND current_round <= 2)`)
- AI prompts must include an explicit instruction: ask ONE concise, targeted challenge question per round; absolute rule — do not grade, do not declare the student correct or incorrect
- Retrieved teaching-material context (if used) must be inside `<sources>...</sources>` boundary
- Student reasoning text is UNTRUSTED input — validate and length-limit before sending to the LLM
- Session is completed after Round 2 — backend must enforce this at the data layer, not only in the UI

## Testing Expectations
- Test that `current_round` cannot exceed 2
- Test that completed sessions reject new messages
- Test that `chk_challenge_one_target` is enforced (exactly one of `reasoning_id` / `review_submission_id`)
- Test that generated challenge responses never contain grades, scores, or pass/fail language (prompt assertion)
