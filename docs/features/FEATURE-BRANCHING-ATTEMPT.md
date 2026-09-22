# Feature: Branching Study Attempt & Retry Model

## 1. Overview & Source of Truth

- **Source of Truth**: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx, lines 35, 59, 76, 84).
- **Core Purpose**: In Branching Study, learning occurs through exploration and iterative decision-making. Students navigate branching scenarios, observe consequences, reflect on outcomes, and may choose to **retry** the scenario to explore alternative paths and strategies.
- **The Concept of an Attempt**:
  - An attempt is an immutable record of one complete or in-progress traversal through a decision tree.
  - Retrying a case creates a **new attempt record** with an incremented `attempt_number`.
  - Past attempts are preserved in history and are never overwritten or mutated retrospectively.

---

## 2. Attempt Data Model

- **Table**: `branching_attempts`
  - `id`: UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  - `student_id`: UUID NOT NULL REFERENCES `users(id)`
  - `case_id`: UUID NOT NULL REFERENCES `cases(id)`
  - `attempt_number`: INTEGER NOT NULL DEFAULT 1
  - `current_node_id`: UUID REFERENCES `case_nodes(id)`
  - `outcome_node_id`: UUID REFERENCES `case_nodes(id)` (set when reaching terminal node)
  - `is_completed`: BOOLEAN NOT NULL DEFAULT FALSE
  - `reflection_text`: TEXT
  - `reflection_status`: VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED' CHECK (reflection_status IN ('NOT_STARTED', 'SUBMITTED'))
  - `reflection_submitted_at`: TIMESTAMPTZ
  - `started_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
  - `updated_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
  - `completed_at`: TIMESTAMPTZ

### Uniqueness & Integrity
```sql
CONSTRAINT uq_branching_attempt_number
    UNIQUE (student_id, case_id, attempt_number)
```

---

## 3. Ownership of Reasoning per Attempt (INV-05, INV-06)

- When a student reaches a Decision Point (`node_id`), selects an option (`selected_option_id`), and provides written justification, this is saved to `student_reasoning`.
- **Structural Owner**: `attempt_id NOT NULL` references `branching_attempts(id)`.
- Reasoning belongs to the student's **attempt**, NOT to the option or node globally.
- If a student retries the case (Attempt 2) and chooses the same option, they submit a new reasoning row under Attempt 2.
- Different students selecting the same option produce independent reasoning rows tied to their own attempts.
- Enforced at database level via `UNIQUE (attempt_id, node_id)`.

---

## 4. Guardrails & Out-of-Scope Concepts

1. **No Comparison Engine**: The platform does NOT run automated semantic diffs, ranking algorithms, or auto-comparison across attempts.
2. **No Attempt Scoring**: There are no scoring columns on `branching_attempts`.
3. **Immutability**: Completed attempts cannot have their historical node choices or reasoning modified.
