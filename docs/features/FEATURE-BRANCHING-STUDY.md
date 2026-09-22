# Feature: Branching Study & Student Reasoning Capture

> **Authoritative Traceability**: Proposal V1.1 (lines 35, 59, 76, 84)  
> **Target Package / Module**: Backend `branching-attempt/`, `reasoning/` · Frontend `pages/student/BranchingCasePlayerPage.tsx`, `pages/student/ReflectionPage.tsx`

---

## 1. Purpose
Provides university students with an active, immersive **Branching Case Player** where they navigate complex dilemma scenarios structured as a decision tree. Rather than passively reading text, students make critical decisions at each situation node (Decision Point), articulate written reasoning justifying each choice per attempt, view lecturer-authored consequences, reach an outcome, reflect, and may optionally retry the scenario to explore alternative paths.

---

## 2. Actors
- **Student**: Navigates branching cases, chooses decision options, provides written reasoning per attempt, reflects upon reaching an outcome, and retries if desired.
- **Lecturer**: Authors/approves case tree nodes and consequences, inspects student reasoning and completion metrics, provides qualitative feedback.
- **Backend Gateway**: Manages `branching_attempts`, verifies case publication status, stores `student_reasoning`, and tracks reflection status.
- **Frontend (BranchingCasePlayerPage)**: Interactive student UI rendering the current situation node, option choices, consequence reveal, reasoning form, and progression controls.

---

## 3. Scope
- Initiating a new attempt (`branching_attempts`) for `PUBLISHED` cases in `BRANCHING_STUDY` mode.
- Presenting Decision Points (situation text, available options).
- Capturing student option selection (`selected_option_id NOT NULL`).
- Capturing written justification (`student_reasoning.reasoning_text`, owned by `attempt_id NOT NULL`).
- Revealing lecturer-authored immediate consequences (`case_options.consequence`).
- Optional AI Reasoning/Challenge Support on the submitted reasoning (max 2 rounds, no grading).
- Advancing the attempt to the next situation node until reaching a terminal outcome node (`outcome_node_id`).
- Student Reflection after outcome (`reflection_text`, `reflection_status`).
- Starting a new attempt (Retry) with incremented `attempt_number`.

---

## 4. Functional Requirements
- **FR-BS-01**: The system shall permit students to start an attempt (`branching_attempts`) for any case in `PUBLISHED` status with `learning_mode = 'BRANCHING_STUDY'`.
- **FR-BS-02**: The player shall present the current node's `situation` and display all available `CaseOption` choices.
- **FR-BS-03**: Upon selecting an option, the student must provide written reasoning (`reasoning_text`) before advancing.
- **FR-BS-04**: The system shall record reasoning in `student_reasoning`, owned strictly by `attempt_id NOT NULL` with `UNIQUE(attempt_id, node_id)`.
- **FR-BS-05**: After reasoning submission, the system reveals the lecturer-authored `consequence` text.
- **FR-BS-06**: The student may optionally engage in AI Reasoning/Challenge Support (max 2 rounds, counter-questions only).
- **FR-BS-07**: When reaching a terminal node (`is_terminal = TRUE`), the attempt records `outcome_node_id` and is marked `is_completed = TRUE`.
- **FR-BS-08**: Upon completion, the student is prompted to write a reflection (`reflection_text`).
- **FR-BS-09**: Students may initiate a retry, creating a new `branching_attempts` record with `attempt_number = previous + 1`.

---

## 5. Main Flow
1. Student navigates to `/student/cases/:caseId/branching-play`.
2. Frontend requests `POST /api/v1/cases/{caseId}/branching-attempts`.
3. Backend creates a record in `branching_attempts` (`attempt_number = 1`, `current_node_id = case.root_node_id`) and returns the root `CaseNode`.
4. Student reads the situation and options at the Decision Point.
5. Student selects an option and enters written reasoning in the justification form.
6. Frontend sends `POST /api/v1/branching-attempts/{attemptId}/reasoning` with `{ nodeId, selectedOptionId, reasoningText }`.
7. Backend validates option belongs to node and stores record in `student_reasoning`.
8. Consequence card is revealed to the student.
9. [Optional] Student interacts with AI Reasoning/Challenge Support (see `FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`).
10. Student clicks "Continue to Next Situation". Attempt advances to `option.next_node_id`.
11. Steps 4–10 repeat until reaching a terminal node (`is_terminal = TRUE`).
12. Terminal outcome is displayed, `outcome_node_id` is recorded, and `is_completed` is set to `TRUE`.
13. Student navigates to `/student/cases/:caseId/attempt/:attemptId/reflect` to submit their reflection.
14. Student may return to case dashboard or click "Retry Case" to start Attempt #2.

---

## 6. Business Rules & Invariants
- **INV-01**: Students cannot access cases that are not `PUBLISHED`.
- **INV-05**: `student_reasoning.attempt_id` is the structural owner of reasoning. Reasoning belongs to the attempt, not to the option globally.
- **INV-06**: One reasoning record per Decision Point per Attempt (`UNIQUE(attempt_id, node_id)`).
- **INV-07**: `selected_option_id` must belong to `node_id`'s options (service layer validation).
- **INV-12**: Retrying creates a NEW `branching_attempts` row (`attempt_number + 1`); attempts are immutable in retrospect.
- **INV-18**: No automated comparison, ranking, or scoring across attempts.

---

## 7. Data Structures Involved
- `cases` (`learning_mode = 'BRANCHING_STUDY'`, `root_node_id NOT NULL`)
- `case_nodes`, `case_options`
- `branching_attempts` (`attempt_number`, `outcome_node_id`, `reflection_text`, `reflection_status`)
- `student_reasoning` (`attempt_id`, `node_id`, `selected_option_id`, `reasoning_text`)
