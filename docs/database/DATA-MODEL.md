# CaseTree AI — Data Model

**Status**: Aligned with Proposal V1.1 (V2 Migration applied)

---

## 1. Core Relational Tables

| Table | Description | Learning Mode |
|---|---|---|
| `users` | All users: lecturers and students with role RBAC (`LECTURER`, `STUDENT`) | Shared |
| `courses` | Lecturer courses scoped to `lecturer_id` | Shared |
| `teaching_materials` | Uploaded PDF/DOCX materials stored in MinIO, metadata in PostgreSQL | Shared |
| `cases` | Case studies supporting both `BRANCHING_STUDY` and `REVIEW_STUDY` | Shared |
| `case_nodes` | Situation nodes in a decision tree | Branching Study |
| `case_options` | Decision options with consequences connecting nodes in a decision tree | Branching Study |
| `branching_attempts` | Student attempts on Branching Study cases, tracking current node, outcome, and reflection | Branching Study |
| `student_reasoning` | Student written justifications submitted at decision points, owned by attempt | Branching Study |
| `review_study_submissions` | Student submissions for Review Study (proposed solution, reasoning, reflection) | Review Study |
| `challenge_support_sessions` | AI Reasoning / Challenge Support sessions (supports both modes, max 2 rounds) | Both |
| `challenge_messages` | Messages within a challenge support session (`CHALLENGE_SUPPORT`, `STUDENT`) | Both |
| `lecturer_feedback` | Qualitative feedback provided by lecturer on attempts or review submissions | Both |

---

## 2. Vector & RAG Tables (FastAPI AI Service)

| Table | Description |
|---|---|
| `document_chunks` | Parsed text chunks with pgvector embeddings (`vector(1536)` or `vector(768)`), linked to `material_id` and `course_id` |

---

## 3. Key Table Details & Constraints

### 3.1 `cases`
- `learning_mode`: VARCHAR(50) NOT NULL CHECK (`learning_mode IN ('BRANCHING_STUDY', 'REVIEW_STUDY')`)
- `status`: VARCHAR(50) NOT NULL CHECK (`status IN ('DRAFT', 'REVIEWED', 'APPROVED', 'PUBLISHED')`)
- `context_text`: TEXT (Review Study background context/data)
- `problem_text`: TEXT (Review Study problem statement/question)
- `root_node_id`: UUID FK → `case_nodes(id)` (Branching Study root pointer)
- `version`: INTEGER NOT NULL DEFAULT 1

### 3.2 `branching_attempts`
- `attempt_number`: INTEGER NOT NULL DEFAULT 1
- `outcome_node_id`: UUID FK → `case_nodes(id)` (recorded when reaching a terminal node)
- `is_completed`: BOOLEAN NOT NULL DEFAULT FALSE
- `reflection_text`: TEXT
- `reflection_status`: VARCHAR(50) NOT NULL CHECK (`reflection_status IN ('NOT_STARTED', 'SUBMITTED')`)
- `reflection_submitted_at`: TIMESTAMPTZ
- **Constraint**: `uq_branching_attempt_number UNIQUE (student_id, case_id, attempt_number)`

### 3.3 `student_reasoning`
- `attempt_id`: UUID NOT NULL FK → `branching_attempts(id)` ON DELETE CASCADE
- `node_id`: UUID NOT NULL FK → `case_nodes(id)`
- `selected_option_id`: UUID NOT NULL FK → `case_options(id)`
- `reasoning_text`: TEXT NOT NULL
- **Constraint**: `uq_reasoning_per_node UNIQUE (attempt_id, node_id)` (one reasoning per decision point per attempt)

### 3.4 `review_study_submissions`
- `student_analysis`: TEXT (nullable, R2 Confirmed Option A)
- `proposed_solution`: TEXT NOT NULL
- `reasoning_text`: TEXT NOT NULL
- `submission_status`: VARCHAR(50) NOT NULL CHECK (`submission_status IN ('SUBMITTED', 'REVIEWED', 'REFLECTED')`)
- `reflection_text`: TEXT
- `reflection_status`: VARCHAR(50) NOT NULL CHECK (`reflection_status IN ('NOT_STARTED', 'SUBMITTED')`)
- `reflection_submitted_at`: TIMESTAMPTZ
- **Constraint**: `uq_review_submission_per_student_case UNIQUE (student_id, case_id)`

### 3.5 `challenge_support_sessions`
- `reasoning_id`: UUID UNIQUE FK → `student_reasoning(id)` (nullable)
- `review_submission_id`: UUID UNIQUE FK → `review_study_submissions(id)` (nullable)
- `current_round`: INTEGER NOT NULL DEFAULT 0 CHECK (`current_round >= 0 AND current_round <= 2`)
- `is_completed`: BOOLEAN NOT NULL DEFAULT FALSE
- **Constraint**: `chk_challenge_one_target CHECK ((reasoning_id IS NOT NULL AND review_submission_id IS NULL) OR (reasoning_id IS NULL AND review_submission_id IS NOT NULL))`

### 3.6 `challenge_messages`
- `session_id`: UUID NOT NULL FK → `challenge_support_sessions(id)` ON DELETE CASCADE
- `round_number`: INTEGER NOT NULL CHECK (`round_number >= 1 AND round_number <= 2`)
- `role`: VARCHAR(50) NOT NULL CHECK (`role IN ('CHALLENGE_SUPPORT', 'STUDENT')`)
- `content`: TEXT NOT NULL

### 3.7 `lecturer_feedback`
- `lecturer_id`: UUID NOT NULL FK → `users(id)`
- `branching_attempt_id`: UUID FK → `branching_attempts(id)` (nullable)
- `review_submission_id`: UUID FK → `review_study_submissions(id)` (nullable)
- `feedback_text`: TEXT NOT NULL
- **Constraint**: `chk_feedback_one_target CHECK ((branching_attempt_id IS NOT NULL AND review_submission_id IS NULL) OR (branching_attempt_id IS NULL AND review_submission_id IS NOT NULL))`

---

## 4. Migrations

Migrations are maintained in SQL files executed against PostgreSQL:
- Backend migrations directory: `backend/migrations/`
- Infrastructure migrations directory: `infrastructure/postgres/migrations/`
- **V1__init_schema.sql**: Initial baseline schema
- **V2__new_flow_schema.sql**: Proposal V1.1 flow schema (cases extensions, branching_attempts, student_reasoning, review_study_submissions, challenge_support_sessions, challenge_messages, lecturer_feedback)

---

## 5. Naming Convention

- Table names: `snake_case`, plural (e.g., `branching_attempts`, `student_reasoning`)
- Column names: `snake_case` (e.g., `attempt_number`, `current_round`)
- Primary keys: `id UUID DEFAULT uuid_generate_v4()`
- Foreign keys: `<referenced_entity>_id UUID`
- Timestamps: `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`
