# Feature: Course Context & Teaching Materials

> **Authoritative Traceability**: Items 4, 5, 6 (Proposal Section 2 p. 6, Section 4 p. 7, Section 11 p. 16)  
> **Target Package / Module**: Backend `course/`, `material/` · Frontend `features/courses/`, `features/materials/` · Storage MinIO

---

## 1. Purpose
Enables university lecturers to organize their teaching domains by establishing **Course Contexts** and uploading authentic **Teaching Materials** (lecture slides, syllabi, case notes in PDF or DOCX format). Teaching materials are securely archived in MinIO object storage and linked to specific courses as the foundational knowledge base for RAG retrieval and branching case study generation.

---

## 2. Actors
- **Lecturer**: Creates and manages courses; uploads, inspects, and deletes teaching materials.
- **Backend Gateway**: Validates file metadata, writes binary blobs to MinIO, tracks processing status.
- **AI Service**: Ingests files from MinIO for parsing and vector indexing.

---

## 3. Scope
- Course CRUD operations (restricted to course-owning lecturer).
- Teaching material file upload (PDF, DOCX) bound to a course.
- MinIO object storage integration with UUID-based object keys.
- Tracking material ingestion status (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`).
- Material listing and deletion.

---

## 4. Functional Requirements
- **FR-MAT-01**: The system shall allow a lecturer to create a course specifying title, course code, and description.
- **FR-MAT-02**: The system shall restrict course updates and material uploads strictly to the course owner.
- **FR-MAT-03**: The system shall accept material uploads in **PDF** (`application/pdf`) and **DOCX** (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`) formats.
- **FR-MAT-04**: The system shall enforce a configurable maximum upload file size (default 50 MB).
- **FR-MAT-05**: The system shall store raw document binaries in MinIO under bucket `edubranch-materials` using non-guessable object keys.
- **FR-MAT-06**: The system shall record material metadata in PostgreSQL table `teaching_materials` and initiate document processing.

---

## 5. Main Flow
1. Lecturer creates or selects a course from `/lecturer/courses`.
2. Lecturer opens the course materials view at `/lecturer/courses/:courseId/materials`.
3. Lecturer selects a local PDF or DOCX file and submits the upload form.
4. Frontend issues `POST /api/v1/courses/{courseId}/materials` (multipart/form-data) with JWT auth.
5. Backend verifies that the authenticated user is the owner of the course.
6. Backend validates file MIME type, extension, and file size limits.
7. Backend streams the binary data to MinIO object storage.
8. Backend records an entry in `teaching_materials` with `processing_status='PENDING'`.
9. Backend notifies the internal AI Service via `POST /internal/v1/ingestion/process`.
10. Lecturer sees the material listed with a status indicator ("Processing" → "Completed").

---

## 6. Inputs
- Course creation: `name` (string, required), `courseCode` (string, optional), `description` (text, optional).
- Material upload: `file` (binary, required), `courseId` (UUID, path parameter).

---

## 7. Outputs
- Course creation: HTTP 201 with Course DTO (`id`, `name`, `courseCode`, `lecturerId`, `createdAt`).
- Material upload: HTTP 201 with Material DTO (`id`, `originalFilename`, `mimeType`, `sizeBytes`, `processingStatus`, `uploadedAt`).

---

## 8. Business Rules
- **BR-MAT-01**: Only PDF and DOCX file types are allowed; executable, archive, image, or generic text formats must be rejected.
- **BR-MAT-02**: Teaching materials belong strictly to the course they were uploaded to; cross-course material sharing is not permitted in MVP.
- **BR-MAT-03**: Deleting a course cascades deletion or archiving of associated materials and generated cases.
- **BR-MAT-04**: If document processing in the AI Service fails, `processing_status` must be set to `FAILED` and `processing_error` populated.

---

## 9. Permissions
- Role `LECTURER`: Full CRUD on courses and materials owned by the lecturer.
- Role `STUDENT`: Read-only access to published cases within enrolled courses (no direct access to raw teaching materials).

---

## 10. Dependencies
- PostgreSQL `courses` and `teaching_materials` tables.
- MinIO Object Storage (`edubranch-materials` bucket).
- Internal AI Service ingestion endpoint.

---

## 11. Data Involved
- **Table `courses`**:
  - `id`: UUID (PK)
  - `name`: VARCHAR(255) NOT NULL
  - `description`: TEXT
  - `course_code`: VARCHAR(100)
  - `lecturer_id`: UUID NOT NULL REFERENCES users(id)
  - `is_active`: BOOLEAN DEFAULT TRUE
- **Table `teaching_materials`**:
  - `id`: UUID (PK)
  - `original_filename`: VARCHAR(500) NOT NULL
  - `stored_object_key`: VARCHAR(1000) NOT NULL
  - `mime_type`: VARCHAR(100) NOT NULL
  - `size_bytes`: BIGINT
  - `course_id`: UUID NOT NULL REFERENCES courses(id)
  - `uploaded_by`: UUID NOT NULL REFERENCES users(id)
  - `processing_status`: VARCHAR(50) DEFAULT 'PENDING' (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`)
  - `chunk_count`: INTEGER
  - `processing_error`: TEXT

---

## 12. Error / Edge Cases
- File exceeds size limit: Return HTTP 413 Payload Too Large.
- Unsupported file type: Return HTTP 415 Unsupported Media Type.
- Unauthorized lecturer attempting upload to another's course: Return HTTP 403 Forbidden.
- MinIO service outage: Return HTTP 503 Service Unavailable with retry guidance.

---

## 13. Out of Scope
- Direct in-browser document editing (Google Docs / Word Online style).
- Document version branching / git-style file history.
- Scanned OCR processing for non-text PDFs (MVP expects text-extractable PDFs).
- LMS (Canvas/Blackboard) file synchronization.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 4, 5, 6)
- [`docs/architecture/DATA-FLOW.md`](../architecture/DATA-FLOW.md) (Flow 1)
- [`docs/features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`](FEATURE-DOCUMENT-PROCESSING-AND-RAG.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Modules `backend/src/modules/course/` and `material/`, database tables `courses` and `teaching_materials`, MinIO Docker container configuration, and frontend page shells exist; upload controller logic and streaming service remain unimplemented.)*
