# Feature: Lecturer Statistics & Cohort Analytics

> **Authoritative Traceability**: Item 26 (Proposal Section 2 p. 6, Section 4 p. 7, Section 6 p. 10, Table 1 p. 9)  
> **Target Package / Module**: Backend `statistics/` · Frontend `pages/lecturer/StatisticsPage.tsx`, `features/statistics/`

---

## 1. Purpose
Provides university lecturers with clear, focused **Cohort Analytics** on how students navigated their published branching case studies. Gives visibility into which decision branches were most frequently chosen, where student consensus diverged, common reasoning patterns in student arguments, and completion rates across the cohort.

---

## 2. Actors
- **Lecturer**: Views aggregate branch statistics, individual node choice distributions, and student argument submissions.
- **Backend Gateway**: Aggregates decision paths and argument records from PostgreSQL.
- **Frontend (StatisticsPage)**: Presents visual branch distribution charts and an argument inspection table.

---

## 3. Scope
- Aggregate session completion metrics (total started, completed, abandoned).
- Branch choice distribution per `CaseNode` (e.g., 65% Option A vs. 35% Option B).
- Traversal path heatmaps on the decision tree.
- Student argument and debate transcript inspection list.
- Scoped strictly to simple MVP statistics (avoiding complex, bloated analytics dashboards).

---

## 4. Functional Requirements
- **FR-STAT-01**: The system shall allow a lecturer to view statistics for any case study within their owned courses.
- **FR-STAT-02**: The system shall compute the percentage and count of students who chose each `CaseOption` at every `CaseNode`.
- **FR-STAT-03**: The system shall display total student participants, completed simulation sessions, and average debate rounds per argument.
- **FR-STAT-04**: The system shall provide a filtered list of student arguments and debate transcripts for a selected node or option to allow the lecturer to inspect reasoning depth.
- **FR-STAT-05**: The system shall restrict statistics queries strictly to the owning lecturer's courses.

---

## 5. Main Flow
1. Lecturer navigates to `/lecturer/statistics` (or clicks "View Stats" on a published case).
2. Frontend requests `GET /api/v1/cases/{caseId}/statistics`.
3. Backend aggregates database records:
   - Counts from `simulation_sessions` grouped by `is_completed`.
   - Counts from `student_arguments` grouped by `node_id` and `option_id`.
   - Average rounds from `debate_sessions`.
4. Backend returns aggregated statistics payload to Frontend.
5. Frontend renders:
   - Top summary cards: Total Students, Completion Rate, Most Contested Node.
   - Tree node breakdown: Visual bar / pie chart showing option percentage split at each decision point.
   - Expandable argument drawer: Lecturer clicks on Option A to read the actual justifications submitted by students.

---

## 6. Inputs
- Query: `caseId` (UUID, path parameter), optional `courseId` (UUID).

---

## 7. Outputs
- Statistics DTO:
  ```json
  {
    "caseId": "uuid",
    "caseTitle": "Supply Chain Dilemma",
    "totalSessions": 45,
    "completedSessions": 42,
    "completionRate": 0.93,
    "nodes": [
      {
        "nodeId": "uuid-node-0",
        "situationSummary": "Unethical supplier discovered",
        "options": [
          { "optionId": "uuid-opt-1", "text": "Terminate contract", "count": 28, "percentage": 62.2 },
          { "optionId": "uuid-opt-2", "text": "Audit supplier", "count": 17, "percentage": 37.8 }
        ]
      }
    ]
  }
  ```

---

## 8. Business Rules
- **BR-STAT-01**: Statistics must only reflect data from `PUBLISHED` cases.
- **BR-STAT-02**: A lecturer can only view statistics for their own courses; cross-lecturer data access is strictly prohibited.
- **BR-STAT-03**: Statistics must remain lightweight and focused on pedagogical insight (branch choices and reasoning quality), not invasive surveillance.

---

## 9. Permissions
- Role `LECTURER`: Read-only access to statistics for owned courses.
- Role `STUDENT`: Strictly forbidden from accessing lecturer statistics endpoints.

---

## 10. Dependencies
- PostgreSQL relational tables `cases`, `case_nodes`, `case_options`, `simulation_sessions`, `student_arguments`, `debate_sessions`.

---

## 11. Data Involved
- Read-only aggregations over existing simulation and argument tables. No separate warehouse table required for MVP scale.

---

## 12. Error / Edge Cases
- No sessions yet for a published case: Return zero counts gracefully (`totalSessions: 0`) without divide-by-zero errors.
- Case has multiple versions: Aggregate by case version or present cumulative data clearly.
- Unauthorized lecturer access attempt: Return HTTP 403 Forbidden.

---

## 13. Out of Scope
- Predictive AI analytics forecasting student exam grades based on simulator choices.
- Real-time live websocket dashboards showing student clicks second-by-second.
- Cross-institution benchmarking.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Item 26)
- [`docs/architecture/DATA-FLOW.md`](../architecture/DATA-FLOW.md) (Flow 6)
- [`docs/features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`](FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Frontend `StatisticsPage.tsx` view shell and backend package structure exist; SQL aggregation queries and statistics service remain unimplemented.)*
