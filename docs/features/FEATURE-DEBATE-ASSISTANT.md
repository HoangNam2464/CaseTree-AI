# Feature: AI Debate Assistant (Devil's Advocate)

> **Authoritative Traceability**: Items 24, 25 (Proposal Section 2 p. 6, Section 4 p. 7, Section 7 p. 11, Section 10 p. 14)  
> **Target Package / Module**: AI Service `debate/assistant/` · Backend `debate/` · Frontend `pages/student/DebatePage.tsx`, `features/debate/`

---

## 1. Purpose
Strengthens university students' critical thinking and argument rigor by deploying a real-time **AI Debate Assistant** acting as a **Socratic Devil's Advocate**. When a student submits a justification for a decision, the AI probes vulnerabilities, unexamined trade-offs, and implicit assumptions in the student's reasoning through focused, contextual counter-questioning.

---

## 2. Actors
- **Student**: Reads counter-questions and submits reasoned rebuttals.
- **AI Debate Assistant**: Synthesizes targeted Socratic counter-questions challenging the student's argument.
- **Backend Gateway**: Enforces the strict maximum 2-round limit and persists debate transcripts.
- **Lecturer**: Inspects debate transcripts to evaluate student reasoning depth and critical engagement.

---

## 3. Scope
- Initiating a debate session bound to a specific `StudentArgument`.
- Round 1: AI generates a single, targeted counter-question challenging the student's reasoning.
- Round 2: Student optionally responds; AI provides one final counter-reflection question.
- Strict hard-cap: Exactly 1 to 2 rounds maximum; further interaction is locked.
- Enforcing the absolute AI governance boundaries (no grading, no pass/fail, no academic judgment).

---

## 4. Functional Requirements
- **FR-DEB-01**: The system shall create a `DebateSession` linked to a `StudentArgument` upon student decision submission.
- **FR-DEB-02**: The AI Service shall receive the student's argument, the situation context, the selected option consequence, and optional relevant course material chunks inside `<sources>...</sources>`.
- **FR-DEB-03**: The AI Service shall generate a Socratic counter-question acting as a Devil's Advocate (challenging assumptions and trade-offs).
- **FR-DEB-04**: The system shall allow the student to submit a rebuttal response for Round 2.
- **FR-DEB-05**: The system shall generate a final follow-up counter-question in Round 2, after which the session transitions to `is_completed = TRUE`.
- **FR-DEB-06**: Both the Backend Gateway and FastAPI AI Service shall **strictly enforce a maximum limit of 2 debate rounds**. Any third request shall be rejected with HTTP 400 Bad Request.
- **FR-DEB-07**: The AI Debate Assistant MUST NOT include grades, letter scores (A/B/C), numerical ratings (0–100), pass/fail decisions, or academic integrity judgments in its responses.

---

## 5. Main Flow
1. Student submits an argument for their decision at a CaseNode.
2. Backend creates `DebateSession` with `current_round = 1` and calls `POST /internal/v1/debate/challenge`.
3. AI Service builds the prompt with Devil's Advocate system instructions:
   ```
   "You are a university-level Socratic Devil's Advocate.
    Your goal is to strengthen the student's critical thinking by challenging the weaknesses,
    trade-offs, and unstated assumptions in their argument.
    Ask ONE concise, targeted counter-question.
    ABSOLUTE RULE: Do NOT grade the student. Do NOT say whether they passed or failed.
    Do NOT declare their reasoning correct or incorrect."
   ```
4. LLM returns a single counter-question.
5. Backend saves `DebateMessage` (`role = 'AI_ASSISTANT'`, `round_number = 1`) and returns it to Frontend.
6. Frontend displays the counter-question in a debate dialogue card.
7. **Round 2 (Optional)**:
   - Student enters their rebuttal: *"While that trade-off exists, in the long term..."*
   - Frontend sends `POST /api/v1/debate/{sessionId}/respond`.
   - Backend increments `current_round = 2` and calls AI Service.
   - AI Service generates the final challenging counter-reflection.
   - Backend saves messages and marks `is_completed = TRUE`.
8. UI indicates: *"Debate round concluded. You may now proceed to the next situation."*

---

## 6. Inputs
- Round 1 Trigger: `argumentId` (UUID).
- Round 2 Rebuttal: `sessionId` (UUID), `responseText` (string, e.g., 20–1000 chars).

---

## 7. Outputs
- Round 1 Response: `{ debateId, roundNumber: 1, question: string, isCompleted: false }`.
- Round 2 Response: `{ debateId, roundNumber: 2, question: string, isCompleted: true }`.

---

## 8. Business Rules
- **BR-DEB-01**: **Hard Cap of 2 Rounds**: Enforced at database schema (`current_round`), backend gateway validation, and AI service request validation.
- **BR-DEB-02**: **Zero Autonomous Grading**: The AI is forbidden from evaluating student answers or declaring winners/losers in the debate.
- **BR-DEB-03**: **Single Question Rule**: Each AI turn must ask exactly ONE focused counter-question rather than a laundry list of points.
- **BR-DEB-04**: **Cost & Latency Control**: Capping rounds to 1–2 and using fast LLMs (Gemini Flash / GPT-4o-mini) controls API costs for university classroom pilots.

---

## 9. Permissions
- Role `STUDENT`: Authorized to participate in debate sessions corresponding to their own simulation sessions.
- Role `LECTURER`: Authorized to inspect all student debate transcripts in their courses.

---

## 10. Dependencies
- FastAPI AI Service debate module (`app/debate/`).
- PostgreSQL tables `debate_sessions`, `debate_messages`.
- LLM Provider Abstraction.

---

## 11. Data Involved
- **Table `debate_sessions`**:
  - `id`: UUID (PK)
  - `argument_id`: UUID NOT NULL UNIQUE REFERENCES student_arguments(id)
  - `current_round`: INTEGER NOT NULL DEFAULT 0 (Valid values: 0, 1, 2)
  - `is_completed`: BOOLEAN DEFAULT FALSE
  - `created_at`, `updated_at`: TIMESTAMPTZ
- **Table `debate_messages`**:
  - `id`: UUID (PK)
  - `session_id`: UUID NOT NULL REFERENCES debate_sessions(id) ON DELETE CASCADE
  - `round_number`: INTEGER NOT NULL (1 or 2)
  - `role`: VARCHAR(50) NOT NULL CHECK (role IN ('AI_ASSISTANT', 'STUDENT'))
  - `content`: TEXT NOT NULL
  - `created_at`: TIMESTAMPTZ

---

## 12. Error / Edge Cases
- Student attempts Round 3 submission: Reject with HTTP 400 Bad Request ("Maximum of 2 debate rounds reached").
- Student submits empty or nonsensical rebuttal: AI asks student to clarify how their response addresses the specific trade-off.
- LLM hallucination / grading attempt: System prompt guardrails and post-generation regex check ensure no grading language ("Score: X/10", "Grade: A") is passed to the student.

---

## 13. Out of Scope
- Unrestricted open-ended general chat with the AI assistant.
- Voice-based or real-time streaming audio debate.
- Automated assignment of final marks or gradebook calculation by AI.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 24, 25)
- [`docs/ai/DEBATE-ASSISTANT.md`](../ai/DEBATE-ASSISTANT.md)
- [`docs/architecture/DATA-FLOW.md`](../architecture/DATA-FLOW.md) (Flow 5)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Module `backend/src/modules/debate/`, request schemas in `ai-service/app/debate/schemas/requests.py`, and frontend `DebatePage.tsx` exist; prompt chain and debate controllers remain unimplemented.)*
