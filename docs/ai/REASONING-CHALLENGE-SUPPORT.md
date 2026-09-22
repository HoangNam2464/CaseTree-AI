# CaseTree AI — AI Reasoning & Challenge Support

**Status**: Scaffolded | **Source of Truth**: Proposal V1.1 (lines 40, 63, 78, 86)

---

## Purpose

AI Reasoning/Challenge Support generates focused, contextual challenge questions that probe student reasoning, trade-offs, and implicit assumptions.

It operates strictly under academic guardrails:
- **Questions Only**: Generates probing counter-questions to prompt deeper reflection.
- **NO GRADING**: Strictly NOT a grading system, NOT a pass/fail system, and does NOT score reasoning.
- **Both Learning Modes**: Supports student reasoning in Branching Study and student proposed solutions/reasoning in Review Study.

---

## Flow

```
Student submits written reasoning (Branching Study or Review Study)
        ↓
Backend Gateway creates challenge_support_sessions, calls FastAPI
        ↓
FastAPI receives:
  - student_reasoning
  - case_context (situation or problem statement)
  - optional retrieved teaching material context
        ↓
FastAPI constructs prompt:
  System: "You are an academic AI Reasoning & Challenge Support assistant..."
          "Ask ONE targeted counter-question. Do NOT grade. Do NOT score."
  <sources>
  [retrieved teaching material context, if any]
  </sources>
  User: "Student reasoning: [reasoning_text]"
        ↓
FastAPI generates challenge question (Round 1)
        ↓
Student reads question, optionally submits response
        ↓
FastAPI generates Round 2 challenge question (if student responds)
        ↓
Session is COMPLETED — no further rounds
```

---

## Challenge Round Enforcement

| Round | Trigger | AI Response | Status After |
|---|---|---|---|
| 1 | Student submits reasoning | Challenge question | Round 1 active |
| 2 | Student responds to Round 1 | Final challenge question | COMPLETED |
| 3+ | **BLOCKED** | None (HTTP 400) | N/A |

Enforced at BOTH layers:
- Backend Gateway: rejects requests when `current_round >= 2`
- FastAPI AI Service: validates `round_number <= 2` in Pydantic schema

---

## AI Governance Invariants

1. **Teaching Material is Untrusted Data**: Always wrap in `<sources>...</sources>` boundary to prevent prompt injection.
2. **No Grading Fields**: Neither request nor response schemas contain score, grade, or rating fields.
3. **No Overrides**: Sources and student input must never override system prompt instructions.
