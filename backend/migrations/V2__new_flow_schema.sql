-- ==============================================================================
-- Edu-Branch-AI — V2 New Flow Schema Migration
-- Source of Truth: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx)
-- All decisions confirmed: 2026-09-22
-- ==============================================================================
-- Summary of changes from V1:
--   1.  cases                      — ADD: learning_mode, context_text, problem_text
--   2.  branching_attempts         — NEW: replaces simulation_sessions
--   3.  student_reasoning          — NEW: replaces student_arguments
--   4.  challenge_support_sessions — NEW: replaces debate_sessions
--                                          supports BOTH Branching Study AND Review Study
--   5.  challenge_messages         — NEW: replaces debate_messages
--   6.  review_study_submissions   — NEW: Review Study student submissions
--   7.  lecturer_feedback          — NEW: Lecturer Review/Feedback artifact
--   8.  Old table retirement       — rename to _deprecated_*, drop in reverse FK order (commented)
-- ==============================================================================

-- ==============================================================================
-- STEP 1: Extend `cases`
-- ==============================================================================
ALTER TABLE cases
    ADD COLUMN learning_mode  VARCHAR(50) NOT NULL DEFAULT 'BRANCHING_STUDY'
        CHECK (learning_mode IN ('BRANCHING_STUDY', 'REVIEW_STUDY')),
    ADD COLUMN context_text   TEXT,    -- REVIEW_STUDY: context/data for students
    ADD COLUMN problem_text   TEXT;    -- REVIEW_STUDY: the problem/question to analyze

-- Application-layer invariants:
--   * BRANCHING_STUDY cases: root_node_id must be set before status -> PUBLISHED
--   * REVIEW_STUDY cases:    context_text + problem_text must be set before PUBLISHED
--   * REVIEW_STUDY cases:    root_node_id remains NULL (no decision tree)

CREATE INDEX idx_cases_learning_mode ON cases(learning_mode);

-- ==============================================================================
-- STEP 2: branching_attempts (replaces simulation_sessions)
-- ==============================================================================
-- Represents one Branching Study attempt by a student for a specific case.
-- Retry = new row with attempt_number incremented. Attempts are never mutated
-- in retrospect; no automatic comparison or scoring across attempts.
CREATE TABLE branching_attempts (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id              UUID NOT NULL REFERENCES users(id),
    case_id                 UUID NOT NULL REFERENCES cases(id),
    attempt_number          INTEGER NOT NULL DEFAULT 1,
    current_node_id         UUID REFERENCES case_nodes(id),
    outcome_node_id         UUID REFERENCES case_nodes(id),  -- NULL until terminal reached
    is_completed            BOOLEAN NOT NULL DEFAULT FALSE,
    reflection_text         TEXT,
    reflection_status       VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED'
                                CHECK (reflection_status IN ('NOT_STARTED', 'SUBMITTED')),
    reflection_submitted_at TIMESTAMPTZ,
    started_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at            TIMESTAMPTZ,
    CONSTRAINT uq_branching_attempt_number
        UNIQUE (student_id, case_id, attempt_number)
);

CREATE INDEX idx_attempts_student_id   ON branching_attempts(student_id);
CREATE INDEX idx_attempts_case_id      ON branching_attempts(case_id);
CREATE INDEX idx_attempts_student_case ON branching_attempts(student_id, case_id);

-- ==============================================================================
-- STEP 3: student_reasoning (replaces student_arguments)
-- ==============================================================================
-- Reasoning is OWNED by the Attempt, not by the Option.
--
-- selected_option_id is NOT NULL:
--   Branching Study flow is always: Select Option -> Own Reasoning.
--   There is no state where a student provides reasoning without first
--   selecting an option at a Decision Point.
--
-- No student_id or case_id columns: derivable via JOIN to branching_attempts.
--
-- UNIQUE(attempt_id, node_id):
--   Enforces one reasoning entry per Decision Point per Attempt.
--   Different students selecting the same option produce different rows
--   under their respective attempt_id values.
--
-- selected_option_id must belong to node_id's options:
--   Enforced at application service layer (not a simple FK constraint).
CREATE TABLE student_reasoning (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    attempt_id          UUID NOT NULL REFERENCES branching_attempts(id) ON DELETE CASCADE,
    node_id             UUID NOT NULL REFERENCES case_nodes(id),
    selected_option_id  UUID NOT NULL REFERENCES case_options(id),
    reasoning_text      TEXT NOT NULL,
    submitted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_reasoning_per_node UNIQUE (attempt_id, node_id)
);

CREATE INDEX idx_reasoning_attempt_id ON student_reasoning(attempt_id);

-- ==============================================================================
-- STEP 4: review_study_submissions (NEW)
-- ==============================================================================
-- Represents a Review Study student submission for a specific case.
-- One submission per student per Review Study case (MVP) enforced via UNIQUE constraint.
-- Several reasonable solutions are accepted; system does not determine
-- a single correct answer or reasoning.
--
-- submission_status transitions (application-layer enforced, forward-only):
--   SUBMITTED -> REVIEWED (when lecturer writes feedback)
--   REVIEWED  -> REFLECTED (when student submits reflection)
--
-- Review-Point R2 (CONFIRMED OPTION A):
-- Proposal V1.1 describes "analyze" as part of the student's reasoning process (lines 37, 61),
-- not a separate mandatory submission artifact.
-- student_analysis remains nullable (TEXT).
CREATE TABLE review_study_submissions (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id              UUID NOT NULL REFERENCES users(id),
    case_id                 UUID NOT NULL REFERENCES cases(id),
    student_analysis        TEXT,            -- nullable: optional distinct analysis field
    proposed_solution       TEXT NOT NULL,
    reasoning_text          TEXT NOT NULL,
    submission_status       VARCHAR(50) NOT NULL DEFAULT 'SUBMITTED'
                                CHECK (submission_status IN ('SUBMITTED', 'REVIEWED', 'REFLECTED')),
    reflection_text         TEXT,
    reflection_status       VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED'
                                CHECK (reflection_status IN ('NOT_STARTED', 'SUBMITTED')),
    reflection_submitted_at TIMESTAMPTZ,
    submitted_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_review_submission_per_student_case
        UNIQUE (student_id, case_id)
);

CREATE INDEX idx_rs_submissions_student_id ON review_study_submissions(student_id);
CREATE INDEX idx_rs_submissions_case_id    ON review_study_submissions(case_id);

-- ==============================================================================
-- STEP 5: challenge_support_sessions (replaces debate_sessions)
-- ==============================================================================
-- Represents one AI Reasoning/Challenge Support interaction on a piece of
-- student reasoning. Supports BOTH learning modes:
--   - Branching Study: linked via reasoning_id -> student_reasoning
--   - Review Study:    linked via review_submission_id -> review_study_submissions
--
-- Exactly ONE of (reasoning_id, review_submission_id) must be NOT NULL.
-- Enforced by chk_challenge_one_target CHECK constraint.
--
-- Round enforcement: max 2 rounds, challenge questions only.
-- No grading, no scoring, no academic right/wrong determination.
CREATE TABLE challenge_support_sessions (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reasoning_id         UUID UNIQUE REFERENCES student_reasoning(id),          -- nullable
    review_submission_id UUID UNIQUE REFERENCES review_study_submissions(id),   -- nullable
    current_round        INTEGER NOT NULL DEFAULT 0
                             CHECK (current_round >= 0 AND current_round <= 2),
    is_completed         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_challenge_one_target CHECK (
        (reasoning_id IS NOT NULL AND review_submission_id IS NULL) OR
        (reasoning_id IS NULL     AND review_submission_id IS NOT NULL)
    )
);

CREATE INDEX idx_challenge_reasoning_id    ON challenge_support_sessions(reasoning_id)
    WHERE reasoning_id IS NOT NULL;
CREATE INDEX idx_challenge_submission_id   ON challenge_support_sessions(review_submission_id)
    WHERE review_submission_id IS NOT NULL;

-- ==============================================================================
-- STEP 6: challenge_messages (replaces debate_messages)
-- ==============================================================================
CREATE TABLE challenge_messages (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id   UUID NOT NULL REFERENCES challenge_support_sessions(id) ON DELETE CASCADE,
    round_number INTEGER NOT NULL CHECK (round_number >= 1 AND round_number <= 2),
    role         VARCHAR(50) NOT NULL
                     CHECK (role IN ('CHALLENGE_SUPPORT', 'STUDENT')),
    content      TEXT NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_challenge_msg_session_id ON challenge_messages(session_id);

-- ==============================================================================
-- STEP 7: lecturer_feedback (NEW)
-- ==============================================================================
-- Lecturer Review/Feedback on student work. Supports BOTH learning modes:
--   - Branching Study: branching_attempt_id NOT NULL, review_submission_id NULL
--   - Review Study:    review_submission_id NOT NULL, branching_attempt_id NULL
--
-- Exactly ONE of (branching_attempt_id, review_submission_id) must be NOT NULL.
-- Full DB-level referential integrity via real PostgreSQL FKs.
-- AI does not grade; no scoring columns.
--
-- Review-Point R3: student_id and case_id are NOT stored on this table.
-- They are derivable via JOIN to branching_attempts or review_study_submissions.
CREATE TABLE lecturer_feedback (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lecturer_id          UUID NOT NULL REFERENCES users(id),
    branching_attempt_id UUID REFERENCES branching_attempts(id),
    review_submission_id UUID REFERENCES review_study_submissions(id),
    feedback_text        TEXT NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_feedback_one_target CHECK (
        (branching_attempt_id IS NOT NULL AND review_submission_id IS NULL) OR
        (branching_attempt_id IS NULL     AND review_submission_id IS NOT NULL)
    )
);

CREATE INDEX idx_feedback_lecturer_id    ON lecturer_feedback(lecturer_id);
CREATE INDEX idx_feedback_attempt_id     ON lecturer_feedback(branching_attempt_id)
    WHERE branching_attempt_id IS NOT NULL;
CREATE INDEX idx_feedback_submission_id  ON lecturer_feedback(review_submission_id)
    WHERE review_submission_id IS NOT NULL;

-- ==============================================================================
-- STEP 8: Old table retirement (COMMENTED OUT)
-- ==============================================================================
-- The repository is confirmed skeleton-only (no business data).
-- Strategy: rename to _deprecated_ prefix -> validate all V2 references -> drop.
--
-- Drop order MUST follow reverse FK dependency to avoid FK violations:
--   1. _deprecated_debate_messages    (FK: session_id -> debate_sessions)
--   2. _deprecated_debate_sessions    (FK: argument_id -> student_arguments)
--   3. _deprecated_student_arguments  (FK: session_id -> simulation_sessions)
--   4. _deprecated_simulation_sessions
--
-- These statements are COMMENTED OUT.
-- Run manually ONLY after verifying:
--   (a) tsc --noEmit passes in frontend/ (no old type references)
--   (b) grep confirms zero app-code hits for deprecated tables
--   (c) All module renames are complete
-- ==============================================================================
-- ALTER TABLE debate_messages     RENAME TO _deprecated_debate_messages;
-- ALTER TABLE debate_sessions     RENAME TO _deprecated_debate_sessions;
-- ALTER TABLE student_arguments   RENAME TO _deprecated_student_arguments;
-- ALTER TABLE simulation_sessions RENAME TO _deprecated_simulation_sessions;
--
-- DROP TABLE _deprecated_debate_messages;
-- DROP TABLE _deprecated_debate_sessions;
-- DROP TABLE _deprecated_student_arguments;
-- DROP TABLE _deprecated_simulation_sessions;
