# EduBranch AI — AI Debate Assistant

**Status**: Scaffolded

---

## Purpose

The AI Debate Assistant is a **Devil's Advocate** tool that challenges student arguments
at decision nodes in the case simulator.

It is strictly NOT a grading system, NOT a pass/fail system, and NOT an academic judgment tool.

---

## Flow

```
Student selects an option at a CaseNode
        ↓
Student submits written justification (StudentArgument)
        ↓
Backend Gateway creates DebateSession, calls FastAPI
        ↓
FastAPI receives:
  - student_argument
  - case_context (node situation + option consequence)
  - optional retrieved teaching material context
  ↓
FastAPI constructs prompt:
  System: "You are a Socratic Devil's Advocate for a university case study..."
          "Ask ONE targeted counter-question. Do NOT grade. Do NOT determine pass/fail."
  <sources>
  [retrieved teaching material context, if any]
  </sources>
  User: "Student argument: [argument_text]"
        ↓
FastAPI generates counter-question (Round 1)
        ↓
Student reads counter-question, submits response
        ↓
FastAPI generates Round 2 counter-question (if student responds)
        ↓
Session is COMPLETED — no further rounds
```

---

## Debate Round Enforcement

| Round | Trigger | AI Response | Status After |
|-------|---------|-------------|--------------|
| 1 | Student submits argument | Counter-question | Round 1 active |
| 2 | Student responds to Round 1 | Counter-question | COMPLETED |
| 3+ | **BLOCKED** | None | N/A |

Round enforcement is at BOTH layers:
- Backend Gateway: rejects API calls when currentRound >= DEBATE_MAX_ROUNDS
- FastAPI: validates round number in request schema

---

## AI Governance — Absolute Rules

> ⚠️ These rules MUST be reflected in the system prompt and enforced in code:

1. The Debate Assistant MUST NOT assign grades (no A/B/C or 0–10 scoring)
2. The Debate Assistant MUST NOT determine if a student''s answer is correct or incorrect
3. The Debate Assistant MUST NOT make pass/fail academic decisions
4. The Debate Assistant MUST ask ONE targeted counter-question per round
5. The Debate Assistant MUST stop after 2 rounds maximum
6. Retrieved teaching context MUST be in `<sources>` boundary

Academic evaluation is the exclusive responsibility of the human lecturer.
