# Edu-Branch-AI — System Data Flows & Sequences

> **Document Status**: Authoritative Architecture Specification  
> **Source of Truth**: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx)  
> **Purpose**: Traces end-to-end data flows and lifecycle sequences across system components for both learning modes (Branching Study & Review Study).

---

## 1. Flow 1: Teaching Material Upload & Document Processing

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend
    participant BE as Backend Gateway
    participant S3 as MinIO (Object Storage)
    participant AI as FastAPI AI Service
    participant DB as PostgreSQL + pgvector

    Lecturer->>FE: Uploads PDF / DOCX file
    FE->>BE: POST /api/v1/courses/{courseId}/materials (Multipart Form)
    BE->>BE: Validate file extension & MIME type
    BE->>S3: PutObject(bucket="casetree-materials", key=file_uuid)
    BE->>DB: INSERT INTO teaching_materials (status='PENDING')
    BE->>AI: POST /internal/v1/ingestion/process (material_id, s3_key, course_id)
    AI->>S3: GetObject(key=file_uuid)
    AI->>AI: Parse text (PyPDF / python-docx)
    AI->>AI: Split into chunks (RecursiveCharacterTextSplitter)
    AI->>AI: Generate embeddings (text-embedding-004 / text-embedding-3-small)
    AI->>DB: INSERT INTO document_chunks (chunk_text, embedding, metadata)
    AI-->>BE: 200 OK (chunk_count=N, status='COMPLETED')
    BE->>DB: UPDATE teaching_materials SET processing_status='COMPLETED', chunk_count=N
    BE-->>FE: 200 OK (Material processed successfully)
```

---

## 2. Flow 2: AI Case Draft Generation (RAG + Structured Output)

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend
    participant BE as Backend Gateway
    participant AI as FastAPI AI Service
    participant DB as PostgreSQL + pgvector
    participant LLM as LLM Provider (Gemini / OpenAI)

    Lecturer->>FE: Clicks "Generate Case Draft" (provides topic hint, material selection)
    FE->>BE: POST /api/v1/cases/generate (courseId, materialIds, topic)
    BE->>AI: POST /internal/v1/generation/generate-case (course_id, material_ids, topic)
    AI->>AI: Generate query embedding for topic
    AI->>DB: Cosine similarity query over document_chunks (WHERE course_id=... ORDER BY embedding <=> query LIMIT 5)
    DB-->>AI: Top-K context chunks
    AI->>AI: Format prompt: System Persona + <sources>[chunks]</sources> + User Prompt
    AI->>LLM: generate_content(prompt, response_schema=DecisionTreeOutput)
    LLM-->>AI: Structured JSON decision tree
    AI->>AI: Validate JSON schema & BFS cycle detection (no loops, no orphans, terminal exists)
    AI-->>BE: 200 OK (Validated DecisionTree JSON)
    BE->>DB: INSERT INTO cases (learning_mode='BRANCHING_STUDY', status='DRAFT', title, ...)
    BE->>DB: INSERT INTO case_nodes & case_options
    BE-->>FE: 201 Created (Case draft generated in DRAFT status)
    FE->>Lecturer: Renders decision tree in review editor
```

---

## 3. Flow 3: Lecturer Review, Edit & Publishing Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend (ReactFlow)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Lecturer->>FE: Reviews case in editor (ReactFlow for Branching; text form for Review Study)
    Lecturer->>FE: Modifies content (nodes/options for Branching; context/problem for Review)
    FE->>BE: PUT /api/v1/cases/{caseId}
    BE->>BE: Validate integrity (tree DAG / non-empty fields)
    BE->>DB: UPDATE cases SET status='REVIEWED' (and update nodes/text)
    BE-->>FE: 200 OK (Updated)
    Lecturer->>FE: Clicks "Approve Case"
    FE->>BE: POST /api/v1/cases/{caseId}/approve
    BE->>DB: UPDATE cases SET status='APPROVED'
    BE-->>FE: 200 OK
    Lecturer->>FE: Clicks "Publish to Students"
    FE->>BE: POST /api/v1/cases/{caseId}/publish
    BE->>BE: Enforce publication invariants (INV-02 / INV-03)
    BE->>DB: UPDATE cases SET status='PUBLISHED'
    BE-->>FE: 200 OK (Case now accessible to students)
```

---

## 4. Flow 4: Branching Study (Player, Attempt, Reasoning, Outcome, Reflection & Retry)

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant FE as React Frontend (BranchingCasePlayerPage)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Student->>FE: Starts Branching Case (/student/cases/:caseId/branching-play)
    FE->>BE: POST /api/v1/cases/{caseId}/branching-attempts
    BE->>DB: Verify case status is PUBLISHED
    BE->>DB: INSERT INTO branching_attempts (student_id, case_id, attempt_number=1, current_node_id=root_node_id)
    BE-->>FE: 200 OK (root CaseNode: situation, options)
    
    loop At each Decision Point
        Student->>FE: Selects Option, enters written reasoning per attempt
        FE->>BE: POST /api/v1/branching-attempts/{attemptId}/reasoning (nodeId, selectedOptionId, reasoningText)
        BE->>DB: INSERT INTO student_reasoning (attempt_id, node_id, selected_option_id, reasoning_text)
        BE->>DB: UPDATE branching_attempts SET current_node_id=option.next_node_id
        BE-->>FE: 200 OK (Reveals lecturer-authored consequence card)
        opt Optional Challenge Support
            FE->>BE: Initiate Challenge Support (see Flow 6)
        end
    end

    Note over Student,DB: Student reaches terminal node (is_terminal=TRUE)
    BE->>DB: UPDATE branching_attempts SET outcome_node_id=terminalNodeId, is_completed=TRUE
    FE->>Student: Displays final outcome summary
    Student->>FE: Navigates to Reflection (/student/cases/:caseId/attempt/:attemptId/reflect)
    Student->>FE: Submits reflection text
    FE->>BE: POST /api/v1/branching-attempts/{attemptId}/reflection (reflectionText)
    BE->>DB: UPDATE branching_attempts SET reflection_text=..., reflection_status='SUBMITTED'
    BE-->>FE: 200 OK

    opt Student Decides to Retry
        Student->>FE: Clicks "Retry Case"
        FE->>BE: POST /api/v1/cases/{caseId}/branching-attempts (starts Attempt #2)
        BE->>DB: INSERT INTO branching_attempts (attempt_number=2, ...)
    end
```

---

## 5. Flow 5: Review Study (Context/Data, Problem, Submission, Feedback & Reflection)

```mermaid
sequenceDiagram
    autonumber
    actor Student
    actor Lecturer
    participant FE as React Frontend (ReviewStudyPage)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Student->>FE: Opens Review Study Case (/student/cases/:caseId/review-study)
    FE->>BE: GET /api/v1/cases/{caseId}
    BE-->>FE: 200 OK (context_text, problem_text)
    Student->>FE: Enters analysis (optional), proposed solution, and reasoning
    FE->>BE: POST /api/v1/cases/{caseId}/review-study/submissions
    BE->>DB: INSERT INTO review_study_submissions (student_id, case_id, student_analysis, proposed_solution, reasoning_text, submission_status='SUBMITTED')
    BE-->>FE: 201 Created (Submission recorded)

    Lecturer->>FE: Inspects submissions (/lecturer/cases/:caseId/feedback)
    Lecturer->>FE: Enters feedback text
    FE->>BE: POST /api/v1/lecturer-feedback (reviewSubmissionId, feedbackText)
    BE->>DB: INSERT INTO lecturer_feedback (lecturer_id, review_submission_id, feedback_text)
    BE->>DB: UPDATE review_study_submissions SET submission_status='REVIEWED'
    BE-->>FE: 201 Created

    Student->>FE: Views feedback (/student/cases/:caseId/review-study/:submissionId/feedback)
    Student->>FE: Writes reflection on lecturer feedback
    FE->>BE: POST /api/v1/review-study/submissions/{submissionId}/reflection (reflectionText)
    BE->>DB: UPDATE review_study_submissions SET reflection_text=..., reflection_status='SUBMITTED', submission_status='REFLECTED'
    BE-->>FE: 200 OK
```

---

## 6. Flow 6: AI Reasoning & Challenge Support (Both Modes)

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant FE as React Frontend (ChallengeSupportPage)
    participant BE as Backend Gateway
    participant AI as FastAPI AI Service
    participant LLM as LLM Provider (Gemini / OpenAI)
    participant DB as PostgreSQL

    FE->>BE: POST /api/v1/challenge-support/start (reasoningId OR reviewSubmissionId)
    BE->>DB: INSERT INTO challenge_support_sessions (reasoning_id OR review_submission_id, current_round=1)
    BE->>AI: POST /internal/v1/challenge-support/question (student_reasoning, case_context, round=1)
    AI->>AI: System Prompt: "You are an AI Reasoning & Challenge Support assistant. Ask 1 challenge question. NO GRADING."
    AI->>LLM: Generate counter-question
    LLM-->>AI: Single targeted challenge question
    AI-->>BE: 200 OK (counter_question)
    BE->>DB: INSERT INTO challenge_messages (role='CHALLENGE_SUPPORT', round_number=1, content=counter_question)
    BE-->>FE: 200 OK (Displays Round 1 question)
    
    opt Student Responds (Round 2)
        Student->>FE: Enters response
        FE->>BE: POST /api/v1/challenge-support/{sessionId}/respond (response_text)
        BE->>DB: INSERT INTO challenge_messages (role='STUDENT', round_number=2, content=response_text)
        BE->>AI: POST /internal/v1/challenge-support/question (student_response, round=2)
        AI->>LLM: Generate final challenge question
        LLM-->>AI: Final question
        AI-->>BE: 200 OK (final_question)
        BE->>DB: INSERT INTO challenge_messages (role='CHALLENGE_SUPPORT', round_number=2, content=final_question)
        BE->>DB: UPDATE challenge_support_sessions SET current_round=2, is_completed=TRUE
        BE-->>FE: 200 OK (Session completed — hard cap 2 rounds enforced)
    end
```

---

## 7. Flow 7: Basic Learning-Flow Statistics

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend (StatisticsPage)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Lecturer->>FE: Navigates to Case Statistics (/lecturer/statistics)
    FE->>BE: GET /api/v1/cases/{caseId}/statistics
    BE->>DB: Query completion rates (branching_attempts.is_completed)
    BE->>DB: Query branch distributions (student_reasoning.selected_option_id)
    BE->>DB: Query attempt distributions (branching_attempts.attempt_number)
    BE->>DB: Query terminal outcomes (branching_attempts.outcome_node_id)
    BE->>DB: Query progression status (reflection_status / submission_status)
    BE-->>FE: 200 OK (Aggregated metrics DTO)
    FE->>Lecturer: Renders summary cards and distribution breakdowns
```
