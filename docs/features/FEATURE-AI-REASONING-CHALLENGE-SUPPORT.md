# Feature: AI Reasoning & Challenge Support

> **Authoritative Traceability**: Proposal V1.1 (lines 40, 63, 78, 86)  
> **Target Package / Module**: AI Service `challenge_support/` · Backend `challenge-support/` · Frontend `pages/student/ChallengeSupportPage.tsx`

---

## 1. Purpose
Strengthens university students' critical thinking and reasoning rigor by deploying **AI Reasoning/Challenge Support**. When a student submits written reasoning justifying a decision in Branching Study or a proposed solution in Review Study, the AI probes trade-offs, unexamined assumptions, and potential blind spots through focused, contextual counter-questions.

---

## 2. Core Pedagogical Principles
1. **Support Function, Not an Independent Platform**: Challenge Support is an embedded assistant invoked within the student's learning flow. It is **not** a standalone debate platform or separate learning mode.
2. **Challenge Questions Only**: The AI generates probing counter-questions to prompt deeper reflection.
3. **No Grading or Scoring**: The AI does NOT evaluate pass/fail, assign grades, score reasoning, or declare answers correct or incorrect.
4. **Strict Round Cap**: Enforced to a maximum of **1–2 rounds** to prevent open-ended chatbot drift.

---

## 3. Scope & Learning Mode Support (Review-Point 2)
AI Reasoning/Challenge Support supports student reasoning across **both** learning modes:
- **Branching Study**: Probes `student_reasoning` submitted at a Decision Point.
- **Review Study**: Probes `proposed_solution` and `reasoning_text` submitted in `review_study_submissions`.

---

## 4. Functional Requirements
- **FR-CS-01**: The system shall create a `challenge_support_sessions` record linked to either a `student_reasoning` row or a `review_study_submissions` row.
- **FR-CS-02**: Exactly one target (`reasoning_id` or `review_submission_id`) must be set per session (`chk_challenge_one_target`).
- **FR-CS-03**: The AI Service shall receive student reasoning, case context, and relevant teaching material chunks wrapped in `<sources>...</sources>`.
- **FR-CS-04**: The AI Service shall generate a targeted challenge question challenging assumptions and highlighting trade-offs.
- **FR-CS-05**: The student may optionally submit a rebuttal or clarification response for Round 2.
- **FR-CS-06**: Round 2 produces one final follow-up question, after which the session is marked `is_completed = TRUE`.
- **FR-CS-07**: Both backend and AI service shall enforce a hard cap of **2 rounds maximum** (`CHECK (current_round >= 0 AND current_round <= 2)`).
- **FR-CS-08**: The AI service MUST NOT include grades, letter scores, numerical ratings, or academic pass/fail decisions.

---

## 5. Main Flow
1. Student submits written reasoning in Branching Case Player or Review Study page.
2. Backend creates `challenge_support_sessions` with `current_round = 1`.
3. Backend calls AI Service `POST /internal/v1/challenge-support/question` with `ChallengeRequest`.
4. AI Service builds the prompt:
   ```
   "You are an academic AI Reasoning and Challenge Support assistant for university students.
    Your goal is to provoke critical reflection by questioning assumptions and trade-offs.
    Ask ONE concise, targeted challenge question.
    ABSOLUTE RULE: Do NOT grade the student. Do NOT declare answers correct or incorrect."
   ```
5. AI Service returns `ChallengeResponse` containing `counter_question`.
6. Backend persists `challenge_messages` (`role = 'CHALLENGE_SUPPORT'`, `round_number = 1`).
7. Student reads counter-question in the challenge support interface.
8. [Round 2 - Optional]: Student submits a response. Backend increments `current_round = 2`, calls AI Service for one final follow-up question, and locks the session as completed.

---

## 6. Data Structures Involved
- **Table `challenge_support_sessions`**:
  - `id`: UUID (PK)
  - `reasoning_id`: UUID UNIQUE REFERENCES `student_reasoning(id)` (nullable)
  - `review_submission_id`: UUID UNIQUE REFERENCES `review_study_submissions(id)` (nullable)
  - `current_round`: INTEGER NOT NULL DEFAULT 0 CHECK (current_round >= 0 AND current_round <= 2)
  - `is_completed`: BOOLEAN NOT NULL DEFAULT FALSE
  - Ràng buộc: `CONSTRAINT chk_challenge_one_target CHECK (...)`
- **Table `challenge_messages`**:
  - `id`: UUID (PK)
  - `session_id`: UUID NOT NULL REFERENCES `challenge_support_sessions(id)` ON DELETE CASCADE
  - `round_number`: INTEGER NOT NULL CHECK (round_number >= 1 AND round_number <= 2)
  - `role`: VARCHAR(50) NOT NULL CHECK (role IN ('CHALLENGE_SUPPORT', 'STUDENT'))
  - `content`: TEXT NOT NULL
