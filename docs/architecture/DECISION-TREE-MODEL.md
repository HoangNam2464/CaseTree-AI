# CaseTree AI — Decision Tree Domain Model

**Status**: Scaffolded | **Source of Truth**: Proposal V1.1

---

## 1. Overview

The decision tree is the core data structure of CaseTree AI for `BRANCHING_STUDY` mode.
A Case is composed of CaseNodes connected by CaseOptions.

## 2. Entity Model

```
Case
├── id: UUID
├── title: String
├── description: String
├── course_id: UUID → Course
├── created_by: UUID → User (LECTURER)
├── learning_mode: CaseLearningMode (BRANCHING_STUDY | REVIEW_STUDY)
├── context_text: TEXT?     ← Review Study background data
├── problem_text: TEXT?     ← Review Study problem statement
├── status: CaseStatus (DRAFT | REVIEWED | APPROVED | PUBLISHED)
├── version: int
├── root_node_id: UUID? → CaseNode (Branching Study only)
└── nodes: List<CaseNode>

CaseNode
├── id: UUID
├── case_id: UUID → Case
├── situation: TEXT          ← The scenario shown to the student
├── is_terminal: boolean     ← True = leaf node, no options
├── node_index: int
└── options: List<CaseOption>

CaseOption
├── id: UUID
├── node_id: UUID → CaseNode
├── text: TEXT               ← The decision choice text
├── consequence: TEXT        ← The immediate outcome shown after selection
└── next_node_id: UUID?      ← NULL = terminal path; FK → CaseNode (same Case)
```

## 3. Structural Invariants

1. **No orphan nodes**: Every node (except root) must be reachable from rootNode
2. **No invalid references**: next_node_id must refer to a CaseNode in the same Case
3. **No cycles**: DFS 3-color cycle detection must pass before case can be saved
4. **At least one terminal**: Every decision tree must have at least one terminal path
5. **Root node is valid**: root_node_id must point to an existing CaseNode in the Case

## 4. JSON Representation (AI Output Format)

```json
{
  "title": "Supply Chain Ethics Dilemma",
  "description": "A case study on ethical sourcing decisions.",
  "root_node_index": 0,
  "nodes": [
    {
      "situation": "Your company discovers a key supplier uses unethical labor practices. What do you do?",
      "options": [
        {
          "text": "Immediately terminate the contract",
          "consequence": "Immediate supply disruption but strong ethical signal.",
          "next_node_index": 1
        },
        {
          "text": "Issue a warning and request an audit",
          "consequence": "Supplier relations maintained but risk of public backlash if leaked.",
          "next_node_index": 2
        }
      ]
    },
    {
      "situation": "The termination caused a 3-month production delay. How do you handle customer communication?",
      "options": [
        {
          "text": "Be fully transparent with customers",
          "consequence": "Loss of some orders but enhanced long-term brand trust.",
          "next_node_index": null
        }
      ]
    },
    {
      "situation": "The audit reveals systemic issues. Do you continue or terminate?",
      "options": [
        {
          "text": "Terminate after the audit period",
          "consequence": "Clean conscience, but faces same supply disruption as Option A.",
          "next_node_index": null
        }
      ]
    }
  ]
}
```

## 5. Case Lifecycle Flow

```
AI Generator produces DRAFT case
          ↓
Lecturer reviews (DRAFT)
          ↓
Lecturer edits nodes/options (DRAFT)
          ↓
Lecturer marks as REVIEWED
          ↓
Lecturer approves (APPROVED)
          ↓
Lecturer publishes (PUBLISHED)
          ↓
Students access Branching Case Player
```

Students can ONLY see cases in PUBLISHED status.
