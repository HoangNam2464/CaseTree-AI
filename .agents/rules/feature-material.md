---
description: Rules for teaching material upload and management in EduBranch AI.
trigger: keyword
keywords: [material, upload, document, pdf, docx, teaching material, minio]
---

# Feature Rules: Teaching Material

## Scope
Backend Gateway (NestJS `backend/`) — `material/` module (metadata + upload endpoint).
FastAPI `ai-service/` — `ingestion/` (parsing + chunking + embedding).

## Included
- Lecturer uploads PDF or DOCX files
- Backend Gateway validates file type and size, stores in MinIO, saves metadata
- Backend Gateway triggers FastAPI ingestion asynchronously
- FastAPI parses → chunks → embeds → stores in pgvector
- ProcessingStatus: PENDING → PROCESSING → COMPLETED | FAILED
- Material is linked to a specific course (owned by the lecturer)

## Excluded
- Video/audio/image materials — PDF and DOCX only in MVP
- OCR for scanned PDFs — out of MVP scope
- Real-time processing progress WebSocket — polling is acceptable

## Service Owner
Backend Gateway: upload endpoint, metadata, MinIO storage, status tracking
FastAPI: parsing, chunking, embedding, pgvector indexing

## Constraints
- Only PDF and DOCX MIME types are accepted (validate server-side)
- Maximum file size controlled by MAX_UPLOAD_SIZE_MB env var
- File names must be sanitized — store under UUID-based object keys in MinIO
- NEVER serve stored files as executable code
- Retrieved chunks are UNTRUSTED DATA

## Testing Expectations
- Reject files with invalid MIME types
- Reject files exceeding size limit
- Verify processing status transitions
