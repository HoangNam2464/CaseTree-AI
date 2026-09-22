# Feature: Student Reflection

## 1. Overview & Source of Truth

- **Source of Truth**: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx, lines 35, 37, 60, 61, 76, 77).
- **Core Purpose**: Reflection is a core pedagogical artifact in CaseTree AI. It encourages meta-cognitive learning, allowing students to evaluate their decision path or solution justification in hindsight.
- **Support Across Both Modes**:
  1. **Branching Study**: Triggered after reaching a terminal outcome node (`outcome_node_id`). Students reflect on the chain of decisions, trade-offs, and resulting outcome before deciding whether to attempt the case again.
  2. **Review Study**: Triggered after the lecturer reviews the submission and provides feedback (`lecturer_feedback`). Students reflect on the feedback, critique their proposed solution, and note areas of improvement.

---

## 2. Lifecycle & State Machine

```
NOT_STARTED (Default)
       │
       ▼ (Student submits reflection text)
   SUBMITTED
```

- In Branching Study, `reflection_status` is tracked on `branching_attempts`.
- In Review Study, `reflection_status` is tracked on `review_study_submissions`. When reflection is submitted, `submission_status` transitions from `REVIEWED` to `REFLECTED`.

---

## 3. Storage Model

### In Branching Study (`branching_attempts` table)
- `reflection_text`: TEXT (nullable until submitted)
- `reflection_status`: VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED' CHECK (reflection_status IN ('NOT_STARTED', 'SUBMITTED'))
- `reflection_submitted_at`: TIMESTAMPTZ (set upon submission)

### In Review Study (`review_study_submissions` table)
- `reflection_text`: TEXT (nullable until submitted)
- `reflection_status`: VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED' CHECK (reflection_status IN ('NOT_STARTED', 'SUBMITTED'))
- `reflection_submitted_at`: TIMESTAMPTZ (set upon submission)

---

## 4. Governance & AI Isolation

1. **No AI Grading of Reflection**: AI models are NEVER used to score, judge, or grade student reflections.
2. **Pedagogical Ownership**: Reflections are accessible to the lecturer for qualitative review and to the student for self-assessment across attempts.
