# Feature: Branching Study — Experiential Decision Journey

> **Authoritative Traceability**: Proposal V1.1 (lines 35, 59, 76, 84) · Product Direction V2 (Edu-Branch-AI)
> **Target Package / Module**: Backend `branching-attempt/`, `reasoning/` · Frontend `pages/student/BranchingCasePlayerPage.tsx`, `pages/student/BranchingReviewPage.tsx`, `pages/student/ReflectionPage.tsx`

---

## 1. Purpose

Provides university students with an immersive, experience-first **Branching Case Player** where they navigate realistic decision scenarios structured as a decision tree. Students make consecutive decisions without interruption — no reasoning forms, no consequence cards between choices — completing the entire journey before entering a structured **REVIEW phase**. In the Review, students look back at every decision they made, understand how each choice shaped the outcome, write retrospective reasoning for key decisions, and reflect. They may then retry with a new attempt to explore a different path.

> **Core pedagogical principle**: Experience first → Complete journey → REVIEW → Reflection → Retry.
> The Branching Study is NOT a quiz. It is a simulated situational experience followed by structured retrospective analysis.

---

## 2. Actors

- **Student**: Navigates branching cases by making consecutive choices until reaching the terminal node, then reviews the full journey, writes reasoning in retrospect, reflects, and may retry.
- **Lecturer**: Authors/approves case tree nodes, options, and outcomes; inspects student attempt paths and reasoning from the REVIEW phase; provides qualitative feedback.
- **Backend Gateway**: Manages `branching_attempts`, verifies case publication status, stores `student_reasoning` (captured post-journey), and tracks reflection status.
- **Frontend (BranchingCasePlayerPage + BranchingReviewPage)**: Renders the experience player (current situation, options, seamless transitions) and the post-journey REVIEW interface (full path visualization, retrospective reasoning forms).

---

## 3. Scope

- Initiating a new attempt (`branching_attempts`) for `PUBLISHED` cases in `BRANCHING_STUDY` mode.
- Presenting Decision Points: situation text and available options.
- Recording student option selection (`selected_option_id`) and advancing seamlessly to the next node.
- **No consequence card is shown mid-flow** — the next situation's context implicitly reflects the consequence.
- Reaching a terminal node ends the journey and transitions to the REVIEW phase.
- **REVIEW phase**: Student sees full path replay — all decision points visited, options chosen, alternatives available, and how choices shaped the outcome. Student writes reasoning retrospectively.
- Student Reflection after REVIEW (`reflection_text`, `reflection_status`).
- Optional AI Reasoning / Challenge Support on student's reasoning (max 2 rounds, counter-questions only, no grading).
- Starting a new attempt (Retry) creates a new `branching_attempts` record.

---

## 4. Functional Requirements

- **FR-BS-01**: The system shall permit students to start an attempt (`branching_attempts`) for any case in `PUBLISHED` status with `learning_mode = 'BRANCHING_STUDY'`.
- **FR-BS-02**: The player shall present the current node's `situation` text and all available `CaseOption` choices clearly.
- **FR-BS-03**: Upon selecting an option, the system advances seamlessly to the next situation. **No reasoning form, no consequence card, and no other block appears between consecutive Decision Points during the Experience phase.**
- **FR-BS-04**: The system records the student's option selection per node in `student_reasoning` (`attempt_id`, `node_id`, `selected_option_id`). The `reasoning_text` field remains null until the REVIEW phase.
- **FR-BS-05**: When reaching a terminal node (`is_terminal = TRUE`), the attempt is marked `is_completed = TRUE` and `outcome_node_id` is recorded. The student is automatically transitioned to the REVIEW phase.
- **FR-BS-06**: In the **REVIEW phase**, the system presents the full journey in order: every Decision Point visited, the option the student chose, alternatives not taken, and the full consequence/outcome text (revealed here for the first time).
- **FR-BS-07**: In the **REVIEW phase**, the student may write reasoning for individual decision points retrospectively. Writing reasoning is encouraged but not required for every single node — emphasis should be on pivotal decisions and outcome-influencing choices.
- **FR-BS-08**: The student submits an overall Reflection (`reflection_text`) at the end of the REVIEW phase.
- **FR-BS-09**: The student may optionally engage in AI Reasoning / Challenge Support (max 2 rounds, counter-questions only, no grading or pass/fail).
- **FR-BS-10**: Students may initiate a retry, creating a new `branching_attempts` record with `attempt_number = previous + 1`. A retry starts the Experience phase from the root node.

---

## 5. Main Flow

### Phase 1 — Experience (No interruptions)

1. Student opens link to `/student/cases/:caseId/branching-play`.
2. Frontend sends `POST /api/v1/cases/{caseId}/branching-attempts`.
3. Backend creates `branching_attempts` (`attempt_number = 1`, `current_node_id = case.root_node_id`) and returns the root `CaseNode`.
4. Student reads the initial situation and context/data. They see the available options.
5. Student selects an option. Frontend sends `POST /api/v1/branching-attempts/{attemptId}/select` with `{ nodeId, selectedOptionId }`.
6. Backend records `student_reasoning` row (`attempt_id`, `node_id`, `selected_option_id`, `reasoning_text = null`). Advances `current_node_id` to `option.next_node_id`. Returns next `CaseNode`.
7. **No consequence card is displayed. No reasoning form blocks the flow.** Student is shown the next situation immediately.
8. Steps 4–7 repeat at each Decision Point until a terminal node is reached.
9. Backend sets `is_completed = TRUE`, records `outcome_node_id`.
10. Frontend transitions to **Phase 2 — REVIEW**.

### Phase 2 — REVIEW (Post-journey retrospective)

11. Student navigates to `/student/cases/:caseId/attempt/:attemptId/review`.
12. Frontend fetches the complete attempt journey: all nodes visited, options chosen, alternatives at each point, and consequence/outcome texts (now revealed).
13. The REVIEW interface shows the full path as a sequential timeline or visual replay:
    - Each Decision Point: situation shown → option chosen (highlighted) → alternatives available → consequence of that choice → next situation.
    - Key moments are surfaced: decisions that significantly affected the outcome.
14. At each Decision Point in the REVIEW, the student may write reasoning: "Why I chose this" / "What I would change" — forms are optional per node but encouraged for pivotal decisions.
15. Frontend sends `PATCH /api/v1/branching-attempts/{attemptId}/reasoning/{nodeId}` with `{ reasoningText }` when student fills in reasoning.

### Phase 3 — Reflection & Retry

16. Student navigates to `/student/cases/:caseId/attempt/:attemptId/reflect`.
17. Student submits overall `reflection_text`.
18. [Optional] AI Reasoning / Challenge Support: Socratic counter-questions based on student's reasoning (max 2 rounds).
19. [Optional] Student clicks "Try Another Path" → Backend creates new attempt (`attempt_number + 1`) → Returns to Phase 1.

---

## 6. Business Rules & Invariants

- **INV-01**: Students cannot access cases that are not `PUBLISHED`.
- **INV-02**: No consequence card, reasoning form, or any blocking step appears during the Experience phase (between Decision Points).
- **INV-03**: Consequences, outcome texts, and full decision analysis are only presented in the REVIEW phase.
- **INV-04**: Number of Decision Points is variable per case — determined by the case structure, not by the system. No fixed count is imposed.
- **INV-05**: `student_reasoning.attempt_id` is the structural owner of reasoning. Reasoning belongs to the attempt, not globally.
- **INV-06**: One reasoning record per Decision Point per Attempt (`UNIQUE(attempt_id, node_id)`). `reasoning_text` is null during Experience, updated in REVIEW.
- **INV-07**: `selected_option_id` must belong to `node_id`'s options (service layer validation).
- **INV-08**: Retrying creates a NEW `branching_attempts` row (`attempt_number + 1`). Attempts are immutable in retrospect.
- **INV-09**: No automated comparison, ranking, or scoring across attempts.
- **INV-10**: AI Challenge Support does not grade, score, or determine pass/fail. Counter-questions only.

---

## 7. Data Structures Involved

- `cases` (`learning_mode = 'BRANCHING_STUDY'`, `root_node_id NOT NULL`)
- `case_nodes` (`situation`, `context_data`, `is_terminal`, `outcome_text`)
- `case_options` (`option_text`, `consequence`, `next_node_id`)
- `branching_attempts` (`attempt_number`, `current_node_id`, `outcome_node_id`, `is_completed`, `reflection_text`, `reflection_status`)
- `student_reasoning` (`attempt_id`, `node_id`, `selected_option_id`, `reasoning_text`) — `reasoning_text` populated in REVIEW phase, not mid-flow
