# Feature: Interactive Case Simulator & Student Argument Capture

> **Authoritative Traceability**: Items 20, 21, 22, 23 (Proposal Section 2 p. 6, Section 4 p. 7, Section 6 p. 10)  
> **Target Package / Module**: Backend `simulation/`, `argument/` · Frontend `pages/student/SimulatorPage.tsx`, `features/simulator/`

---

## 1. Purpose
Provides university students with an active, immersive **Interactive Case Simulator** where they role-play decision-making in branching scenarios. Rather than passively reading text, students make critical decisions at each situation node, view immediate real-world consequences of their choices, and are required to articulate a concise written justification/argument for each choice made.

---

## 2. Actors
- **Student**: Traverses the case study, selects decisions, views consequences, and writes reasoning arguments.
- **Backend Gateway**: Manages simulation sessions, verifies publication status, records decisions and arguments.
- **Frontend (SimulatorPage)**: Interactive student UI rendering the current situation node, option cards, consequence reveal, and argument input form.

---

## 3. Scope
- Initializing simulation sessions for published cases.
- Step-by-step node presentation (situation text, available decision options).
- Capturing student option selection (`StudentDecision`).
- Revealing the immediate consequence corresponding to the selected option.
- Capturing student written justification/argument (minimum length enforced).
- Triggering the AI Debate Assistant upon argument submission.
- Advancing the simulation session to the next node until reaching a terminal state.

---

## 4. Functional Requirements
- **FR-SIM-01**: The system shall permit enrolled students to start a simulation session for any case in `PUBLISHED` status.
- **FR-SIM-02**: The simulator shall present the current node's `situation` and display all available `CaseOption` choices.
- **FR-SIM-03**: Upon student selection of an option, the system shall display the immediate `consequence` text.
- **FR-SIM-04**: The system shall require the student to submit a short written justification (`argument_text`) explaining the rationale behind their decision before progressing.
- **FR-SIM-05**: The system shall record the argument in `student_arguments` table, linked to the `simulation_sessions` record, node, and selected option.
- **FR-SIM-06**: After argument submission, the system shall transition to the AI Debate Assistant modal or next situation node.
- **FR-SIM-07**: When the student reaches a node with `is_terminal = TRUE` (or an option where `next_node_id = NULL`), the session shall be marked as completed (`is_completed = TRUE`).

---

## 5. Main Flow
1. Student navigates to `/student/cases/:caseId/simulate`.
2. Frontend requests `POST /api/v1/cases/{caseId}/simulation/start`.
3. Backend creates a record in `simulation_sessions` with `current_node_id = case.root_node_id` and returns the root `CaseNode`.
4. Student reads the initial dilemma situation and reviews Option A and Option B.
5. Student clicks "Select Option A".
6. The UI reveals Option A's immediate consequence card.
7. An argument input field appears: *"Explain your reasoning for choosing this action (50–500 words)."*
8. Student types justification and clicks "Submit Argument".
9. Frontend sends `POST /api/v1/simulation/{sessionId}/decision` with `{ nodeId, optionId, argumentText }`.
10. Backend saves the `StudentArgument` record and opens a `DebateSession`.
11. The AI Debate Assistant challenges the student's argument (see `FEATURE-DEBATE-ASSISTANT.md`).
12. Once the debate round concludes, the student clicks "Continue to Next Situation".
13. Backend updates `simulation_sessions.current_node_id = option.next_node_id`.
14. Simulator loads the next situation node.
15. If the next node is terminal, simulator presents final outcome summary and marks session complete.

---

## 6. Inputs
- Start Session: `caseId` (UUID).
- Submit Decision: `sessionId` (UUID), `nodeId` (UUID), `optionId` (UUID), `argumentText` (string, required, e.g., 20–2000 chars).

---

## 7. Outputs
- Current Node State: `{ nodeId, situation, options: [{ id, text }], isTerminal: boolean }`.
- Consequence & Argument Confirmation: `{ argumentId, consequenceText, debateAvailable: boolean }`.
- Session Summary: `{ sessionId, isCompleted: boolean, pathTaken: [{ nodeTitle, optionChosen, consequence }] }`.

---

## 8. Business Rules
- **BR-SIM-01**: **No Blind Skipping**: A student cannot advance to the next node without submitting an argument justifying their choice.
- **BR-SIM-02**: **Immutable Decision Path**: Once an argument is submitted for a node, the decision at that node cannot be altered during that active session.
- **BR-SIM-03**: **Access Gated to Published**: Sessions cannot be initiated for non-published cases under any circumstances.
- **BR-SIM-04**: **Argument Privacy**: A student's arguments are visible only to that student and the lecturer of the course.

---

## 9. Permissions
- Role `STUDENT`: Authorized to simulate published cases and submit arguments for their own sessions.
- Role `LECTURER`: Authorized to inspect anonymized or cohort-level simulation progress and argument submissions.

---

## 10. Dependencies
- PostgreSQL tables `simulation_sessions`, `student_arguments`.
- Case Domain Model (`CaseNode`, `CaseOption`).
- Feature Debate Assistant for triggering post-argument debate.

---

## 11. Data Involved
- **Table `simulation_sessions`**:
  - `id`: UUID (PK)
  - `student_id`: UUID NOT NULL REFERENCES users(id)
  - `case_id`: UUID NOT NULL REFERENCES cases(id)
  - `current_node_id`: UUID REFERENCES case_nodes(id)
  - `is_completed`: BOOLEAN DEFAULT FALSE
  - `started_at`, `updated_at`, `completed_at`: TIMESTAMPTZ
- **Table `student_arguments`**:
  - `id`: UUID (PK)
  - `session_id`: UUID NOT NULL REFERENCES simulation_sessions(id)
  - `student_id`: UUID NOT NULL REFERENCES users(id)
  - `case_id`: UUID NOT NULL REFERENCES cases(id)
  - `node_id`: UUID NOT NULL REFERENCES case_nodes(id)
  - `option_id`: UUID NOT NULL REFERENCES case_options(id)
  - `argument_text`: TEXT NOT NULL
  - `submitted_at`: TIMESTAMPTZ

---

## 12. Error / Edge Cases
- Argument too short (< 20 characters): Reject client-side and server-side with validation error "Please elaborate on your reasoning".
- Network interruption during submission: Frontend caches argument in local storage / Zustand until successfully acknowledged.
- Attempting to advance an already completed session: Return HTTP 400 "Simulation session is already finished".

---

## 13. Out of Scope
- Multiplayer concurrent simulation where students take simultaneous collective votes.
- Timed speed-run simulations with countdown clocks.
- Audio/video argument submissions (text only in MVP).

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 20, 21, 22, 23)
- [`docs/architecture/DATA-FLOW.md`](../architecture/DATA-FLOW.md) (Flow 4)
- [`docs/features/FEATURE-DEBATE-ASSISTANT.md`](FEATURE-DEBATE-ASSISTANT.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Modules in `backend/src/modules/simulation/` and `argument/`, database migration schema, and frontend `SimulatorPage.tsx` exist; active simulation session controllers and state transition logic remain unimplemented.)*
