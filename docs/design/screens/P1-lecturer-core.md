# P1 — Core Lecturer Flow

> **Priority**: NOW. Proposal V1.1 frames Branching Study as the MVP's critical path — Case Review here gets the deepest spec of anything in the system.
> **Visual system**: `docs/design/GLOBAL-DESIGN-SYSTEM.md`.
> **Covers**: `/lecturer/courses`, `/lecturer/courses/:courseId/materials`, `/lecturer/courses/:courseId/cases`, `/lecturer/cases/:caseId/review`.

---

## 1. Course Catalog (`/lecturer/courses`)

### Purpose & Function
Entry point for the Lecturer role. Lists owned courses; allows creating a new course (`FEATURE-COURSE-AND-MATERIALS.md` FR-MAT-01).

### User & Context
Lecturer only. First screen after login.

### Layout
Page header ("Courses", `text-display`) + primary button "New Course" (top-right) + grid or table of course cards.

### Data
Per course: `name`, `courseCode`, `description` (truncated), material count, case count (if available cheaply — otherwise omit rather than invent an endpoint).

### Actions
- Create course (opens modal: `name` required, `courseCode` optional, `description` optional).
- Click a course card → `/lecturer/courses/:courseId/materials` (materials is the natural first stop after creating/selecting a course, since cases require materials).

### States
- **Empty**: "No courses yet" + primary "Create your first course" action (§5.11 pattern).
- **Loading**: skeleton course cards.
- **Error**: standard error state, retry.

### Boundary
No cross-lecturer course visibility — a lecturer only ever sees their own courses (`FEATURE-COURSE-AND-MATERIALS.md` BR-MAT-01/FR-MAT-02 ownership rule).

---

## 2. Course Materials (`/lecturer/courses/:courseId/materials`)

### Purpose & Function
Upload and inspect teaching materials (PDF/DOCX) that feed RAG retrieval and case generation (`FEATURE-COURSE-AND-MATERIALS.md`, `FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`).

### Layout
Breadcrumb (Courses → [Course Name] → Materials). Upload control (drag-and-drop zone or file picker button) at top. Materials list/table below.

### Data
Per material: `originalFilename`, `mimeType`, `sizeBytes`, `processingStatus` (`PENDING`/`PROCESSING`/`COMPLETED`/`FAILED`), `chunk_count` (once completed), `uploadedAt`.

### Actions
- Upload file (PDF/DOCX only — reject other types client-side before the request, matching `BR-MAT-01`).
- Delete material (destructive — requires confirmation dialog per `GLOBAL-DESIGN-SYSTEM.md §5.10`; deletion cascades per `BR-MAT-03`, so the confirmation copy must say so plainly).

### States
- **Processing status per row**: `PENDING`/`PROCESSING` show a small inline spinner + muted label; `COMPLETED` shows a `semantic-success` check + chunk count; `FAILED` shows `semantic-error` + the `processing_error` message (plain language, not a raw stack trace).
- **Empty**: "No materials uploaded yet" + prompt to upload.
- **Upload error**: file-too-large (413) → "File exceeds the 50MB limit"; unsupported type (415) → "Only PDF and DOCX files are supported."

### Boundary
No in-browser document editing/preview beyond filename/status (`FEATURE-COURSE-AND-MATERIALS.md §13` — no Google-Docs-style editor). No OCR-scanned-PDF messaging promises — if extraction fails, show the generic processing error only.

---

## 3. Cases List (`/lecturer/courses/:courseId/cases`)

### Purpose & Function
Lists cases for the course, filterable by learning mode, and is where AI case generation is triggered (`FEATURE-CASE-GENERATION.md`).

### Layout
Breadcrumb (Courses → [Course Name] → Cases). Filter tabs or segmented control: **All / Branching Study / Review Study** (§5.6 Tabs pattern, using `mode-branching`/`mode-review` tokens on the active filter). Primary button "Generate Case" (top-right). Case card grid below (Case Card component, `GLOBAL-DESIGN-SYSTEM.md §6.1`).

### Data
Per case (Case Card): `title`, `learning_mode` badge, `status` badge, short `description`, `updatedAt`, AI-origin marker while `status = DRAFT`.

### Actions
- **Generate Case**: opens a modal — `topic` (required text, 10–500 chars per `FR-GEN-01`/inputs table), optional `materialIds` multi-select (sourced from the course's completed materials only), optional `targetNodeCount`. On submit, redirects to `/lecturer/cases/:caseId/review` once the draft is created.
- Click a case card → `/lecturer/cases/:caseId/review`.

### States
- **Generation in progress**: after submitting the Generate Case modal, show a loading state (this can take several seconds — LLM call + validation retries per `FEATURE-CASE-GENERATION.md` FR-GEN-05); do not block the whole screen silently — show a visible "Generating your case…" state, and route to Case Review once ready.
- **Generation failure**: if the AI service exhausts retries (HTTP 502 per §12), show an error toast: "Case generation failed — please try again, or refine your topic." Do not create a broken/partial case record for the lecturer to see.
- **Empty (no materials yet)**: if the course has zero completed materials, disable "Generate Case" and show a hint pointing to the Materials screen first — generation quality depends on ingested material (`FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`), and this is a real prerequisite, not an invented restriction.

### Boundary
Generation is Lecturer-only (`FR-GEN-01`/§9 permissions) — never expose a "Generate Case" affordance anywhere in the Student shell.

---

## 4. Case Review — Decision Tree Editor (`/lecturer/cases/:caseId/review`)

> This is the single most business-critical screen in the product (Proposal V1.1, Discovery Plan §C footnote) — it is the mandatory Human-in-the-Loop gate (`FEATURE-CASE-REVIEW-AND-PUBLISHING.md` BR-REV-01). Give it the deepest spec.

### Purpose & Function
Lets the Lecturer inspect, edit, approve, and publish an AI-generated (or lecturer-authored) case. For `BRANCHING_STUDY` cases: a ReactFlow tree canvas + node-edit side panel. For `REVIEW_STUDY` cases: a simpler form editor (context/problem text) — **no tree**, since Review Study cases have no `case_nodes` (`FEATURE-REVIEW-STUDY.md §4`: "No Decision Tree").

### Layout — Branching Study variant
- Top: Publish/Review Status Stepper (`GLOBAL-DESIGN-SYSTEM.md §6.3`) showing `DRAFT → REVIEWED → APPROVED → PUBLISHED`, plus case title (editable inline) and learning-mode badge.
- Main area: two-pane split — left/center is the ReactFlow canvas (ratio ~65%), right is the node-edit side panel (~35%), collapsible on narrower screens.
- Canvas: Decision Node component per node (`GLOBAL-DESIGN-SYSTEM.md §6.4`); edges represent `CaseOption` → labeled with a short excerpt of the option text.
- Side panel (opens when a node is selected): editable `situation` textarea, list of that node's options — each with editable `option text` and `consequence` textareas, plus a next-node selector (dropdown of existing nodes, or "Mark as terminal outcome").
- Bottom/footer bar (sticky): "Save Changes," "Approve Case," "Publish Case" — buttons enabled/disabled per current status (see Actions below).

### Layout — Review Study variant
- Same status stepper header.
- No canvas. Simple stacked form: `context_text` (large textarea), `problem_text` (large textarea). No node/option editor.
- Same footer action bar (Save / Approve / Publish), same status gating.

### Data
Branching: `title`, `description`, `root_node_id`, per-node `situation`/`is_terminal`, per-option `text`/`consequence`/`next_node_id`. Review: `title`, `description`, `context_text`, `problem_text`.

### Actions
- **Save Changes**: `PUT /api/v1/cases/{caseId}/nodes/{nodeId}` (Branching) or the case-level update endpoint (Review). Any edit to a `DRAFT` case transitions it to `REVIEWED` (`FR-REV-03`) — the stepper should visibly advance the moment a save succeeds, not require a separate explicit step.
- **Approve Case**: enabled once in `REVIEWED` (or `DRAFT`) status; transitions to `APPROVED` (`FR-REV-04`).
- **Publish Case**: enabled only once `APPROVED`; transitions to `PUBLISHED` (`FR-REV-05`) — **always behind a confirmation dialog** (§5.10), since this is the moment students gain access. Confirmation copy should state plainly that the case becomes visible to enrolled students.
- Add/remove/re-link nodes and options directly on the canvas (drag a new edge to re-link `next_node_id`; delete a node prompts re-linking per `BR-REV-03` edge case).

### States
- **Graph validation error** (cycle or orphan introduced by an edit): block save, highlight the offending edge/node in `semantic-error`, inline message ("Cannot save: loop detected" / "This node has no incoming path from the start"). Matches `FEATURE-CASE-REVIEW-AND-PUBLISHING.md §12` exactly — do not invent different wording.
- **Delete-blocked**: deleting a node that other options still point to shows the exact prompt from the feature doc: "Options in Node X point to this node. Please re-link them before deleting."
- **Publish disabled**: if invariants aren't met yet (Branching: no `root_node_id`; Review: empty `context_text`/`problem_text`) the Publish button stays disabled with a tooltip explaining what's missing (`FEATURE-CASE-REVIEW-AND-PUBLISHING.md §11` publication invariants INV-02/INV-03).
- **Read-only awareness for published+active cases**: if a `PUBLISHED` case already has active student attempts, structural edits should surface a warning that this may create a new version rather than silently mutating history (`BR-REV-04`) — exact versioning UX is a backend-driven detail, but the warning itself is a required state.

### Boundary
No collaborative multi-lecturer real-time editing (no presence cursors, no locking UI — `§13` explicitly out of scope). No public marketplace/publish-to-other-universities affordance. The AI never re-generates or auto-fills content on this screen after the initial draft — every field here is lecturer-owned once opened for edit.

---

## Statistics & Feedback Note
`/lecturer/statistics` and `/lecturer/cases/:caseId/feedback` are P3 (LATER) per the confirmed sequencing — see `docs/design/screens/P3-support.md`. Do not build them as part of the P1 pass.
