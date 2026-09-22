# Feature: Lecturer Case Review, Edit & Publishing Workflow

> **Authoritative Traceability**: Items 17, 18, 19 (Proposal Section 2 p. 6, Section 4 p. 7, Section 7 p. 11, Section 10 p. 14)  
> **Target Package / Module**: Backend `case/` · Frontend `pages/lecturer/CaseReviewPage.tsx`, `features/case-review/`

---

## 1. Purpose
Enforces the mandatory **Human-in-the-Loop** governance gate in CaseTree AI. Ensures that AI-generated decision tree cases are never shown directly to university students. A lecturer must inspect the generated situations, options, and consequences, make manual editorial adjustments via an interactive form/canvas editor, formally approve the case, and publish it to the student cohort.

---

## 2. Actors
- **Lecturer**: Inspects, edits, approves, and publishes the decision tree case study.
- **Backend Gateway**: Enforces the case lifecycle state machine (`DRAFT → REVIEWED → APPROVED → PUBLISHED`) and restricts student queries to published cases only.
- **Frontend (CaseReviewPage)**: Combines a ReactFlow decision tree canvas with a side-by-side node editing form.

---

## 3. Scope
- Case lifecycle state machine transitions.
- Interactive node editing (updating situation text, option descriptions, consequence explanations).
- Adding, removing, or re-linking decision options and nodes.
- Re-running graph integrity validation on lecturer edits.
- Approval action (marking status `APPROVED`).
- Publishing action (transitioning to `PUBLISHED` and opening student access).

---

## 4. Functional Requirements
- **FR-REV-01**: The system shall present the lecturer with a visual representation of the decision tree alongside a form editor for individual nodes.
- **FR-REV-02**: The system shall allow the lecturer to edit the title, description, node situations, option texts, and consequence texts.
- **FR-REV-03**: The system shall transition case status to `REVIEWED` whenever manual edits are committed to a `DRAFT` case.
- **FR-REV-04**: The system shall allow the lecturer to approve a case, transitioning status from `REVIEWED` (or `DRAFT`) to `APPROVED`.
- **FR-REV-05**: The system shall allow the lecturer to publish an `APPROVED` case, transitioning status to `PUBLISHED`.
- **FR-REV-06**: The system shall reject student simulation requests for any case with status other than `PUBLISHED` with HTTP 403 Forbidden.

---

## 5. Main Flow
1. Following generation (or from the case list), Lecturer opens `/lecturer/cases/:caseId/review`.
2. Frontend fetches case tree details via `GET /api/v1/cases/{caseId}`.
3. ReactFlow renders the topology (nodes connected by directed option edges).
4. Lecturer clicks on Node #1; the right-hand panel displays editable fields for:
   - Situation scenario text
   - Option A text & consequence
   - Option B text & consequence
5. Lecturer corrects a typo in Option A's consequence and clicks "Save Changes".
6. Frontend issues `PUT /api/v1/cases/{caseId}/nodes/{nodeId}`.
7. Backend updates the node, runs graph integrity checks, and updates case status to `REVIEWED`.
8. Lecturer reviews all terminal branches and clicks "Approve Case".
9. Backend updates status to `APPROVED`.
10. Lecturer clicks "Publish Case". Backend updates status to `PUBLISHED`.
11. The case becomes visible on student dashboards for that course.

---

## 6. Inputs
- Node update: `nodeId` (UUID), `situation` (string), `options` (array of option objects with `text`, `consequence`, `nextNodeId`).
- Lifecycle transitions: `caseId` (path parameter), action (`approve`, `publish`, `unpublish`).

---

## 7. Outputs
- Success: HTTP 200 with updated Case DTO reflecting new status and updated node details.
- Failure: HTTP 400 with graph validation error message if an edit introduces a cycle or orphan node.

---

## 8. Business Rules
- **BR-REV-01**: **Mandatory Human Gate**: AI-generated cases are ALWAYS born in `DRAFT` status and can NEVER bypass human review.
- **BR-REV-02**: **Strict Publication Access**: Under no circumstances may a student account view, query, or simulate a case in `DRAFT`, `REVIEWED`, or `APPROVED` status.
- **BR-REV-03**: **Integrity Preserving Edits**: Edits made by the lecturer must satisfy the same DAG constraints (no cycles, reachability from root) as AI generation.
- **BR-REV-04**: **Immutable Once Active**: Once a student has begun an active simulation session on a `PUBLISHED` case, editing structural nodes should be restricted or trigger a new version (`version = version + 1`) to preserve student argument integrity.

---

## 9. Permissions
- Role `LECTURER`: Full edit, approval, and publication rights on cases within owned courses.
- Role `STUDENT`: Read-only access strictly restricted to cases where `status = 'PUBLISHED'`.

---

## 10. Dependencies
- ReactFlow library for graph visualization.
- Backend case service and database tables `cases`, `case_nodes`, `case_options`.

---

## 11. Data Involved
- **`cases.learning_mode` column (Proposal V1.1)**:
  ```sql
  learning_mode VARCHAR(50) NOT NULL DEFAULT 'BRANCHING_STUDY'
      CHECK (learning_mode IN ('BRANCHING_STUDY', 'REVIEW_STUDY'))
  ```
- **`cases.status` column**:
  ```sql
  CHECK (status IN ('DRAFT', 'REVIEWED', 'APPROVED', 'PUBLISHED'))
  ```
- **Publication Invariants (INV-02, INV-03)**:
  - For `BRANCHING_STUDY`: `root_node_id` must be set and valid before status can transition to `PUBLISHED`.
  - For `REVIEW_STUDY`: `context_text` and `problem_text` must be non-empty before status can transition to `PUBLISHED`.
- **`cases.version` column**: Tracks revision increments.

---

## 12. Error / Edge Cases
- Lecturer introduces a cycle: Validation fails; UI highlights offending edge in red with message "Cannot save: loop detected".
- Lecturer deletes a node that other options point to: System prompts "Options in Node X point to this node. Please re-link them before deleting."
- Student attempts direct URL access to draft case: Backend repository query `WHERE id = :id AND status = 'PUBLISHED'` returns `ResourceNotFoundException` (HTTP 404).

---

## 13. Out of Scope
- Collaborative multi-lecturer concurrent editing (Google Docs style locking).
- Public marketplace publishing to third-party universities.
- Automated publication based on timer/cron without human sign-off.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 17, 18, 19)
- [`docs/architecture/DATA-FLOW.md`](../architecture/DATA-FLOW.md) (Flow 3)
- [`docs/features/FEATURE-DECISION-TREE.md`](FEATURE-DECISION-TREE.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Case lifecycle types in `backend/src/modules/case/`, database CHECK constraints, and frontend review page shell `CaseReviewPage.tsx` exist; form save handlers and publish state machine services remain unimplemented.)*
