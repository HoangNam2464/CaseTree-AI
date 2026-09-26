# Feature: Review Study (Simple MVP)

## 1. Overview & Source of Truth

- **Source of Truth**: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx, lines 37, 61, 77, 85).
- **Core Purpose**: Review Study is one of Edu-Branch-AI's two distinct learning modes. In the MVP, it provides a simple, structured case analysis workflow where students receive case context, relevant data, and an open problem, analyze it, propose their own solution, justify it with reasoning, receive lecturer feedback, and engage in reflection.
- **Fundamental Principle**: Case study education recognizes multiple valid perspectives. The system **does not determine a single correct answer or reasoning**, nor does AI assign grades.

---

## 2. Learning Flow

```
Lecturer Creates/Publishes Case (learning_mode = 'REVIEW_STUDY')
  ↓
Student Views Context & Data (`cases.context_text`)
  ↓
Student Reads Problem/Question (`cases.problem_text`)
  ↓
Student Formulates Analysis (`review_study_submissions.student_analysis` — optional distinct field)
  ↓
Student Submits Proposed Solution (`proposed_solution`) & Reasoning (`reasoning_text`)
  [Optional: AI Reasoning/Challenge Support, max 2 rounds, counter-questions only]
  ↓
Submission Status: SUBMITTED
  ↓
Lecturer Reviews & Enters Feedback (`lecturer_feedback.feedback_text`)
  ↓
Submission Status: REVIEWED
  ↓
Student Reads Feedback & Writes Reflection (`reflection_text`)
  ↓
Submission Status: REFLECTED (reflection_status = 'SUBMITTED')
```

---

## 3. Data Model & Invariants

- **Table**: `review_study_submissions`
  - `id`: UUID primary key
  - `student_id`: UUID REFERENCES `users(id)`
  - `case_id`: UUID REFERENCES `cases(id)`
  - `student_analysis`: TEXT (nullable, R2 = CONFIRMED OPTION A)
  - `proposed_solution`: TEXT NOT NULL
  - `reasoning_text`: TEXT NOT NULL
  - `submission_status`: VARCHAR(50) — `SUBMITTED` → `REVIEWED` → `REFLECTED`
  - `reflection_text`: TEXT
  - `reflection_status`: VARCHAR(50) — `NOT_STARTED` → `SUBMITTED`
  - `reflection_submitted_at`: TIMESTAMPTZ
  - `submitted_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
  - `updated_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Cardinality Constraint**: `CONSTRAINT uq_review_submission_per_student_case UNIQUE (student_id, case_id)`.
  - Exactly **one submission** per student per Review Study case in MVP.
  - There is **no retry / re-submission** in Review Study (unlike Branching Study).

---

## 4. Architectural Boundaries & Guardrails

1. **No Decision Tree**: Review Study cases do NOT use `case_nodes` or `case_options`. `root_node_id` on `cases` is NULL.
2. **No Automated Grading**: AI does NOT evaluate pass/fail or assign numerical scores to student solutions or reasoning.
3. **Lecturer Authority**: Academic review and feedback belong entirely to the course lecturer.
4. **Publication Guard**: Students cannot access Review Study cases that are not in `PUBLISHED` status.
