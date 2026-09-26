# Feature: Lecturer Review & Feedback

## 1. Overview & Source of Truth

- **Source of Truth**: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx, lines 37, 61, 77, 85).
- **Core Purpose**: Edu-Branch-AI maintains lecturer agency as a central pillar. The platform provides a dedicated feedback channel where lecturers evaluate student submissions, offer contextual comments, and guide student learning.
- **Support Across Both Modes**:
  1. **Branching Study**: Lecturer can review a student's completed path, selected options, reasoning per Decision Point, outcome, and reflection on a specific attempt (`branching_attempts`), providing targeted feedback.
  2. **Review Study**: Lecturer reviews the student's proposed solution and reasoning (`review_study_submissions`), providing substantive qualitative feedback before the student reflects.

---

## 2. Data Model & Referential Integrity

- **Table**: `lecturer_feedback`
  - `id`: UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  - `lecturer_id`: UUID NOT NULL REFERENCES `users(id)`
  - `branching_attempt_id`: UUID REFERENCES `branching_attempts(id)` (nullable)
  - `review_submission_id`: UUID REFERENCES `review_study_submissions(id)` (nullable)
  - `feedback_text`: TEXT NOT NULL
  - `created_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()
  - `updated_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW()

### Target Integrity Constraint
```sql
CONSTRAINT chk_feedback_one_target CHECK (
    (branching_attempt_id IS NOT NULL AND review_submission_id IS NULL) OR
    (branching_attempt_id IS NULL     AND review_submission_id IS NOT NULL)
)
```

### Denormalization & Consistency Guard (INV-20)
- `student_id` and `case_id` are **NOT** stored directly on `lecturer_feedback`.
- Storing them redundantly would risk data inconsistency (e.g., mismatched student ID between feedback and attempt).
- To view feedback for a given student or case, backend queries perform an inner join to `branching_attempts` or `review_study_submissions`.

---

## 3. Governance & Academic Role

1. **Lecturer Authority**: All evaluation and feedback are authored by human lecturers.
2. **No AI Grading**: AI is strictly prohibited from generating grade values, pass/fail marks, or automatic feedback evaluations.
3. **Trigger for Reflection**: In Review Study, submitting lecturer feedback transitions the submission status from `SUBMITTED` to `REVIEWED`, enabling the student to write their reflection.
