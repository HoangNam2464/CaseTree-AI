---
description: Rules for the student interactive case simulator in CaseTree AI.
trigger: keyword
keywords: [simulator, simulation, student, decision, node, consequence, navigate, case play]
---

# Feature Rules: Student Interactive Simulator

## Scope
Backend Gateway (NestJS `backend/`) — `simulation/` module.
Frontend — `features/simulator/` (ReactFlow for tree display).

## Included
- Student loads a PUBLISHED case
- Student sees the current situation (node)
- Student sees available options
- Student selects an option → sees consequence → moves to next node
- System detects terminal node (simulation complete)
- Simulation session state persisted (currentNodeId, completion status)
- Student may restart or resume a session

## Excluded
- Student modifying the case or its content
- Skipping nodes or options
- Real-time multi-student interaction in same session

## Service Owner
Backend Gateway: session persistence, node traversal logic
Frontend: decision tree display via ReactFlow, navigation UX

## Constraints
- Only PUBLISHED cases can be loaded
- StudentId is always set from JWT — never trust client-provided studentId
- Simulation session must record: studentId, caseId, currentNodeId, timestamps
- Terminal node detection based on `CaseNode.isTerminal` flag

## Testing Expectations
- Test that non-PUBLISHED cases return 403/404
- Test session creation and node progression
- Test terminal node detection
