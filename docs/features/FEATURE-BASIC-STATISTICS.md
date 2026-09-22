# Feature: Basic Learning-Flow Statistics

> **Authoritative Traceability**: Proposal V1.1 (lines 65, 87)  
> **Target Package / Module**: Backend `statistics/` · Frontend `pages/lecturer/StatisticsPage.tsx`

---

## 1. Purpose
Provides university lecturers with clear, foundational **Learning-Flow Statistics** on how students navigated their published cases. Focuses strictly on meaningful pedagogical metrics defined in Proposal V1.1 without unnecessary analytics complexity.

---

## 2. Core Metrics Defined in Proposal V1.1

1. **Completion**: Proportion and count of student attempts that reached a terminal outcome node (`branching_attempts.is_completed = TRUE`).
2. **Selected Branch**: Distribution and frequency of student choices at each Decision Point (`student_reasoning.selected_option_id` grouped by `case_options`).
3. **Number of Attempts**: Count and distribution of attempts per student per case (`branching_attempts.attempt_number`).
4. **Outcome**: Distribution of terminal outcomes reached by the cohort (`branching_attempts.outcome_node_id`).
5. **Learning-Flow Status**: Current progression state of students:
   - Branching Study: in-progress vs completed vs reflected (`reflection_status`).
   - Review Study: submitted vs reviewed vs reflected (`review_study_submissions.submission_status`).

---

## 3. Scope & Guardrails
- Scoped strictly to the 5 Proposal metrics listed above.
- **Out of scope**: No automated comparison engine, no attempt scoring or ranking, no predictive modeling, no complex multi-tenant analytics dashboards.

---

## 4. Functional Requirements
- **FR-STAT-01**: The system shall allow lecturers to query statistics for any case in their owned courses.
- **FR-STAT-02**: The system shall aggregate branch selection counts at each `case_node` across all attempts.
- **FR-STAT-03**: The system shall compute cohort completion rates and the distribution of final outcomes.
- **FR-STAT-04**: The system shall provide summary metrics on attempt counts (e.g. single-attempt vs retry students).
- **FR-STAT-05**: The system shall display learning-flow status distributions (e.g. pending feedback, reflected).

---

## 5. Main Flow
1. Lecturer navigates to `/lecturer/statistics` (or clicks "View Statistics" on a case).
2. Frontend requests `GET /api/v1/cases/{caseId}/statistics`.
3. Backend aggregates data from:
   - `branching_attempts` (`is_completed`, `attempt_number`, `outcome_node_id`, `reflection_status`)
   - `student_reasoning` (`selected_option_id`, `node_id`)
   - `review_study_submissions` (`submission_status`, `reflection_status` if Review Study)
4. Backend returns clean statistics DTO.
5. Frontend renders summary cards and branch choice breakdowns.
