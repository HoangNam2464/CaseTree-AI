# Feature: AI Case Generator & Structured Output

> **Authoritative Traceability**: Items 9, 10, 11 (Proposal Section 2 p. 6, Section 4 p. 7, Section 6 p. 10, Section 10 p. 14)  
> **Target Package / Module**: AI Service `generation/case_generator/`, `generation/schemas/` · Backend `case/`

---

## 1. Purpose
Empowers university lecturers to automatically transform static teaching materials into rich, interactive **Branching Decision Tree Case Studies** (`learning_mode = 'BRANCHING_STUDY'`). Uses an LLM with **Structured Output** (JSON Schema enforcement) and RAG context to synthesize realistic situations, dilemma options, and immediate consequences grounded in authentic course content.

> **Note on Learning Modes (Proposal V1.1)**: AI Case Generation in this pipeline generates Case Drafts for **Branching Study** (`learning_mode = 'BRANCHING_STUDY'`). Cases for **Review Study** (`learning_mode = 'REVIEW_STUDY'`) focus on `context_text` and `problem_text` without decision trees. Both modes follow the Common Flow: AI+RAG Draft → Lecturer Review/Edit → Lecturer Approve → Publish.

---

## 2. Actors
- **Lecturer**: Triggers generation, specifies topic hints and material context, reviews generated case.
- **Backend Gateway**: Coordinates generation request between Frontend and AI Service; persists generated case in `DRAFT` status.
- **FastAPI AI Service**: Retrieves course chunks, formats prompt with JSON Schema, validates response via Pydantic v2.
- **LLM Provider**: Generates structured JSON matching the decision tree schema (Gemini 2.0 Flash / OpenAI GPT-4o-mini).

---

## 3. Scope
- Prompt assembly using retrieved RAG chunks (`<sources>` boundary).
- Invoking LLM with strict JSON Schema constraints.
- Parsing and validating the output tree structure (detecting cycles, disconnected nodes, missing consequences).
- Automatic re-prompting / retry if validation fails (up to 2 retries).
- Returning validated JSON structure to the Backend Gateway for persistence as a `DRAFT` case.

---

## 4. Functional Requirements
- **FR-GEN-01**: The system shall allow a lecturer to trigger AI case generation for a selected course with optional topic keywords and material selections.
- **FR-GEN-02**: The AI Service shall assemble a prompt including:
  1. System persona (expert case study author for higher education).
  2. Retrieved course context chunks inside `<sources>...</sources>`.
  3. Strict structural instructions (situation, options, consequences, next node references).
- **FR-GEN-03**: The AI Service shall enforce Structured Output using Pydantic v2 schemas (`CaseGenerationOutput`).
- **FR-GEN-04**: The system shall validate the generated decision tree for structural integrity:
  - Root node must exist at index 0.
  - Every non-terminal option must reference a valid node index within the case.
  - Cycle detection (BFS/DFS) must verify that the tree is an acyclic directed graph (DAG).
  - All non-root nodes must be reachable from the root node (no orphan nodes).
  - At least one terminal path must exist.
- **FR-GEN-05**: If validation fails, the AI Service shall re-prompt the LLM with the error detail up to 2 times before failing.
- **FR-GEN-06**: All successfully generated cases shall be saved with status `DRAFT`.

---

## 5. Main Flow
1. Lecturer navigates to `/lecturer/courses/:courseId/cases` and clicks "Generate Case".
2. Lecturer enters a topic prompt (e.g., "Ethical dilemmas in international supply chains") and selects source materials.
3. Frontend sends `POST /api/v1/cases/generate` to Backend Gateway.
4. Backend verifies ownership and forwards request to FastAPI AI Service: `POST /internal/v1/generation/generate-case`.
5. AI Service performs semantic retrieval over `document_chunks` for the topic.
6. AI Service constructs the prompt with `<sources>` boundary and passes `CaseGenerationOutput` schema to LLM.
7. LLM returns structured JSON.
8. AI Service validates JSON against Pydantic schema and runs graph integrity check (`validate_tree_structure`).
9. AI Service returns validated JSON tree to Backend Gateway.
10. Backend Gateway persists `Case` (status `DRAFT`), `CaseNode` records, and `CaseOption` records in PostgreSQL.
11. Backend returns case details to Frontend, redirecting lecturer to the Case Review editor.

---

## 6. Inputs
- `courseId`: UUID (required).
- `topic`: String describing the desired theme or learning objective (required, e.g., 10–500 chars).
- `materialIds`: Optional list of UUIDs to constrain retrieval to specific uploaded documents.
- `targetNodeCount`: Optional target size for the tree (default: 3–7 nodes).

---

## 7. Outputs
- Success: Validated `CaseGenerationOutput` JSON:
  ```json
  {
    "title": "Supply Chain Ethical Crisis",
    "description": "Managing child labor allegations in foreign suppliers.",
    "root_node_index": 0,
    "nodes": [
      {
        "node_index": 0,
        "situation": "An investigative report reveals unverified child labor in your Tier-2 supplier...",
        "is_terminal": false,
        "options": [
          {
            "text": "Immediately terminate the contract",
            "consequence": "Supplier shuts down, but factory workers face sudden unemployment and public blames company.",
            "next_node_index": 1
          },
          {
            "text": "Launch an independent on-site audit",
            "consequence": "Maintains stability while gathering facts, but risks public accusations of delay.",
            "next_node_index": 2
          }
        ]
      },
      ...
    ]
  }
  ```

---

## 8. Business Rules
- **BR-GEN-01**: A generated case is ALWAYS created with status `DRAFT`. It must never be directly published.
- **BR-GEN-02**: The tree must contain NO infinite decision loops; students must be able to progress to a terminal outcome.
- **BR-GEN-03**: The AI must produce realistic university-level dilemmas with legitimate trade-offs, not simplistic right/wrong answers.
- **BR-GEN-04**: Hallucinated content must be minimized by grounding situations in retrieved `<sources>`.

---

## 9. Permissions
- Role `LECTURER`: Authorized to trigger generation within own courses.
- Role `STUDENT`: Strictly forbidden from invoking case generation.

---

## 10. Dependencies
- AI Service provider abstraction (`providers/factory.py`).
- Pydantic v2 schema definitions (`generation/schemas/decision_tree.py`).
- RAG retrieval pipeline (`retrieval/`).
- PostgreSQL persistence (`cases`, `case_nodes`, `case_options`).

---

## 11. Data Involved
- `Case` entity (status `DRAFT`, `version=1`).
- `CaseNode` entities (`situation`, `is_terminal`, `node_index`).
- `CaseOption` entities (`option_text`, `consequence`, `next_node_id`).

---

## 12. Error / Edge Cases
- LLM returns invalid JSON: AI service retries with error feedback; fails with HTTP 502 if retries exhausted.
- Cycle detected in output: AI service rejects and retries generation.
- Disconnected orphan node generated: AI service prunes or regenerates.
- No relevant material found: Fall back to general domain prompt or prompt user to upload more detailed materials.

---

## 13. Out of Scope
- Direct public student generation of cases.
- Real-time streaming generation of tree nodes (MVP generates complete tree atomically).
- Multi-agent debate among multiple LLMs during case authoring.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 9, 10, 11)
- [`docs/architecture/DECISION-TREE-MODEL.md`](../architecture/DECISION-TREE-MODEL.md)
- [`docs/features/FEATURE-DECISION-TREE.md`](FEATURE-DECISION-TREE.md)
- [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](FEATURE-CASE-REVIEW-AND-PUBLISHING.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Pydantic schema `CaseGenerationOutput`, `CaseNodeSchema`, `CaseOptionSchema`, and BFS cycle detection method in `ai-service/app/generation/schemas/decision_tree.py` exist; active LLM prompt chain and generation route remain unimplemented.)*
