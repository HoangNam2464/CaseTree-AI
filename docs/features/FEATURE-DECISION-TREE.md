# Feature: Branching Decision Tree Domain Model

> **Authoritative Traceability**: Items 12, 13, 14, 15, 16 (Proposal Section 2 p. 6, Section 4 p. 7, Section 9 p. 13)  
> **Target Package / Module**: Backend `case/` · AI Service `generation/schemas/` · Frontend `components/tree/`

---

## 1. Purpose
Defines the mathematical and relational domain structure of the **Branching Decision Tree**, the core pedagogical mechanism of CaseTree AI. The decision tree models sequential decision-making under uncertainty through structured nodes (`Situation`), branches (`Options`), immediate feedback (`Consequences`), and directed transitions (`Next Node`).

---

## 2. Actors
- **Lecturer**: Reviews, edits, re-links, or authors decision tree nodes and options.
- **Student**: Traverses the decision tree step-by-step in the simulator.
- **AI Generator**: Synthesizes the initial decision tree topology.
- **System Validator**: Enforces graph invariants (DAG structure, reachability, terminal nodes).

---

## 3. Scope
- Domain entity representation for `Case`, `CaseNode`, and `CaseOption`.
- Graph integrity rules and cycle detection algorithms.
- Node relationships: root node, intermediate dilemma nodes, terminal outcome nodes.
- Option relationships: text, consequence, and `next_node_id` foreign key references.
- Transformation between relational database records, JSON API payloads, and ReactFlow graph objects.

---

## 4. Functional Requirements
- **FR-TREE-01**: A `Case` shall be composed of one root `CaseNode` and one or more child `CaseNode` elements.
- **FR-TREE-02**: A `CaseNode` shall represent a scenario or situation (`situation: TEXT`) presented to the student.
- **FR-TREE-03**: A non-terminal `CaseNode` shall have between 2 and 4 `CaseOption` choices.
- **FR-TREE-04**: Each `CaseOption` shall contain:
  - Decision text (`option_text: TEXT`) describing the action taken.
  - Consequence (`consequence: TEXT`) describing the immediate outcome of that decision.
  - Next node pointer (`next_node_id: UUID?`) pointing to the resulting situation (or NULL if terminal).
- **FR-TREE-05**: A terminal `CaseNode` (`is_terminal = TRUE`) shall have zero outgoing options and represents the conclusion of the case study path.
- **FR-TREE-06**: The system shall validate graph integrity whenever a tree is generated or modified:
  - **Acyclic Property**: No directed path may loop back to a previously visited node.
  - **Reachability**: Every node in the tree must be reachable by at least one path from the root node.
  - **Terminal Existence**: At least one path from the root node must reach a terminal node.
  - **Referential Integrity**: `next_node_id` must reference a node within the same `Case`.

---

## 5. Main Flow
1. **Creation**: The AI Service or Lecturer defines nodes and options with relative indexing.
2. **Validation**: Graph integrity validation runs (BFS cycle detection & reachability check).
3. **Persistence**:
   - Save `Case` record.
   - Batch-save `CaseNode` records.
   - Batch-save `CaseOption` records with foreign keys pointing to `CaseNode.id`.
   - Update `Case.root_node_id` to point to the designated initial node.
4. **Rendering**: Frontend transforms the relational structure into ReactFlow `nodes` and `edges` for visualization.
5. **Traversal**: In simulation, student choices advance the session pointer (`current_node_id = option.next_node_id`).

---

## 6. Inputs
- Case Node Payload: `situation` (string), `is_terminal` (boolean), `options` (array of option objects).
- Case Option Payload: `text` (string), `consequence` (string), `next_node_id` (UUID or null).

---

## 7. Outputs
- Relational entities or serialized tree JSON format.
- Graph validation result: `{ is_valid: boolean, errors: string[] }`.

---

## 8. Business Rules
- **BR-TREE-01**: The database domain model is the absolute source of truth for the decision tree; visual graph coordinates (x, y) are presentation metadata only.
- **BR-TREE-02**: `next_node_id = NULL` explicitly denotes a terminal branch transition.
- **BR-TREE-03**: Orphan nodes (unreachable from the root) are strictly forbidden; if a lecturer deletes an intermediate node, all dangling options must be re-linked or flagged.
- **BR-TREE-04**: Direct self-loops (`node.option.next_node_id == node.id`) are strictly prohibited.

---

## 9. Permissions
- Edit Tree: Restricted to the Lecturer who owns the Course.
- Read Tree Structure: Lecturer (all statuses); Student (only in `PUBLISHED` status, navigated one node at a time).

---

## 10. Dependencies
- PostgreSQL tables `cases`, `case_nodes`, `case_options`.
- ReactFlow library for client-side rendering.

---

## 11. Data Involved
```sql
-- Core structural relationship
Case (1) ────< CaseNode (N)
                 │ (1)
                 └───< CaseOption (N) ────> CaseNode (next_node_id)
```
- Foreign key `case_options.next_node_id REFERENCES case_nodes(id)` enforces relational consistency.

---

## 12. Error / Edge Cases
- Invalid `next_node_id`: If an option references a non-existent node or a node belonging to a different case, throw `ValidationException`.
- Circular dependency: BFS traversal detects visited nodes in active branch; throws `CycleDetectedException`.
- Missing terminal node: If all branches loop or have invalid pointers, validation fails with "No valid terminal outcome found".

---

## 13. Out of Scope
- Dynamic runtime tree generation during a student's active simulation (tree must be static and pre-approved).
- Multi-user real-time branching (where student A's decision alters student B's scenario).

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 12, 13, 14, 15, 16)
- [`docs/architecture/DECISION-TREE-MODEL.md`](../architecture/DECISION-TREE-MODEL.md)
- [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](FEATURE-CASE-REVIEW-AND-PUBLISHING.md)
- [`docs/features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`](FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Module `backend/src/modules/case/`, database tables `cases`, `case_nodes`, `case_options`, and Pydantic validation models exist; graph edit services remain unimplemented.)*
