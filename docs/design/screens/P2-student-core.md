# P2 — Core Student Flow

> **Priority**: NOW. The other half of the MVP-critical loop.
> **Visual system**: `docs/design/GLOBAL-DESIGN-SYSTEM.md`.
> **Covers**: `/student/cases/:caseId/branching-play`, `/student/cases/:caseId/attempt/:attemptId/reflect`, `/student/cases/:caseId/challenge/:sessionId`.

---

## 1. Branching Case Player (`/student/cases/:caseId/branching-play`)

### Purpose & Function
The Branching Study **Experience phase**: seamless, immersive decision-making journey. Student reads each situation, selects an option, and advances to the next situation with no blocking steps in between. The full consequence analysis and reasoning capture happen in the **REVIEW phase** (§1b below), not mid-flow.

### User & Context
Student only. Requires the case to be `PUBLISHED` (`INV-01`) — non-published cases must 404.
Student accesses via a direct link provided by the Lecturer. There is no student browse page.

### Layout
Full-width immersive reading layout (distraction-free decision interface). Top: case title + a subtle progress indicator (e.g. "Decision 2 of ?" — not a percentage bar, since branch length is variable and unknown). Center: current node's `situation` text in a readable, capped-width column (`GLOBAL-DESIGN-SYSTEM.md §3` line-length rule). Below: Option Selector (`§6.5`).

**Important**: After selecting an option, the player advances immediately to the next situation. There is NO reasoning form, NO consequence card, NO delay between Decision Points during the Experience phase.

### Data
`situation` (current node), list of `CaseOption` (`option_text` only — **consequence text is NOT displayed during Experience phase**).

### Flow / States (Experience Phase — matches `FEATURE-BRANCHING-STUDY.md §5 Phase 1`)
1. **Reading**: situation text + option selector shown.
2. **Option selected**: the selected option is briefly highlighted, then the player transitions seamlessly to the next situation (next node). No reasoning form. No consequence reveal.
3. **Advance**: `current_node_id` moves to `option.next_node_id`. Steps 1–2 repeat at each Decision Point.
4. **Terminal reached** (`is_terminal = TRUE`): a distinct Outcome state renders — clearly marks this as the end of the journey, records `outcome_node_id = TRUE`, marks `is_completed = TRUE`. The student is then automatically transitioned to the REVIEW phase (`§1b` below).

### Retry
After Reflection (§2), a "Try Another Path" action creates a new attempt (`attempt_number + 1`, `FR-BS-10`). Retrying must be visually framed as exploring an alternative path, not as "fixing a wrong answer" — there is no wrong answer (Proposal V1.1 guardrail).

### Boundary
No reasoning form between Decision Points. No consequence card between Decision Points. No grading/scoring UI. Consequences are pre-existing lecturer-authored/approved data — never generated live by AI during play.

---

## 1b. Branching REVIEW Phase (`/student/cases/:caseId/attempt/:attemptId/review`)

### Purpose & Function
Post-journey retrospective analysis. After completing the full journey (reaching a terminal node), the student enters the REVIEW phase to look back at every decision they made, understand how each choice shaped the outcome, and write reasoning retrospectively.

### Layout
Full-page sequential timeline view. Each decision point in the journey is shown in order:
- **Situation** text (the scenario they saw)
- **Option chosen** (highlighted; alternatives shown muted)
- **Consequence** of that choice (revealed here for the first time, since it was withheld during Experience)
- **Optional reasoning textarea**: "Why did you choose this? What would you do differently?" — encouraged for pivotal decisions, not required for every single node
- Key moments are surfaced by the system: "This decision significantly affected your outcome."

### Data
Full attempt journey: all `student_reasoning` records for the attempt (with `selected_option_id`), all `case_nodes` and `case_options` visited (including `consequence` texts now revealed), `outcome_node_id`.

### Flow
1. Student sees full journey replay, top to bottom.
2. Student writes reasoning for key decision points (optional per node, encouraged for pivotal ones).
3. Frontend sends `PATCH /api/v1/branching-attempts/{attemptId}/reasoning/{nodeId}` for each filled-in reasoning.
4. Student clicks "Complete Review" → navigates to Reflection (§2).
5. Optional: Challenge Support may be accessed from here if student wants to probe their reasoning further (§3).

### Boundary
Consequences revealed here, never mid-flow. No grading/scoring. No "correct path" framing.

---

## 2. Reflection (`/student/cases/:caseId/attempt/:attemptId/reflect`)

### Purpose & Function
Post-journey meta-cognitive reflection (`FEATURE-REFLECTION.md`). Accessed after the student completes the REVIEW phase.

### Layout
Focused single-column page (not a modal — reflection deserves a full, unhurried writing space). Shows a compact summary of the completed path (optional — e.g. final outcome title) above the Reflection Input (`GLOBAL-DESIGN-SYSTEM.md §6.8`).

### Data
`reflection_text` (student-authored), `reflection_status` (`NOT_STARTED` → `SUBMITTED`).

### Actions
- Submit reflection → `reflection_status = SUBMITTED`, `reflection_submitted_at` set.
- After submission: options to return to the case dashboard or "Retry Case."

### States
- **Already submitted** (student navigates back): show the reflection read-only rather than an editable form — reflections are not described as editable after submission anywhere in the feature doc; treat as append-only unless a future spec says otherwise.

### Boundary
No AI grading or scoring of the reflection text (`FEATURE-REFLECTION.md §4` — "No AI Grading of Reflection").

---

## 3. AI Reasoning / Challenge Support (`/student/cases/:caseId/challenge/:sessionId`)

### Purpose & Function
Optional, cross-mode Socratic challenge on a piece of submitted reasoning — probes assumptions/trade-offs via targeted counter-questions, capped at 2 rounds, never grades (`FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`). In P2 this is entered from the Branching Case Player (§1); the same screen also serves Review Study (`FEATURE-REVIEW-STUDY.md`), but that entry path is documented in `P4-review-study.md`.

### Layout
Challenge Support Panel (`GLOBAL-DESIGN-SYSTEM.md §6.11`): round indicator at top ("Round 1 of 2"), the AI's counter-question rendered as a neutral card with the `ai-support` tag, an optional student response textarea below it for Round 2.

### Data
`challenge_support_sessions.current_round`, `challenge_messages` (`role`, `content`, `round_number`).

### Flow
1. **Round 1**: AI counter-question shown immediately (generated server-side from the student's reasoning + case context + `<sources>`-bounded material — this generation is a backend/AI-service concern, not a UI decision).
2. **Student may respond** (optional) → triggers Round 2: one further AI follow-up question.
3. **Session complete**: after Round 2 (or if the student chooses not to respond and closes out Round 1), the composer is replaced with a "Session complete" state — no further open-ended input is possible (`FR-CS-06`/§6.11).

### States
- **Loading**: while the AI generates a counter-question, show a lightweight loading state within the panel (not a full-page spinner) — this is a support panel embedded in the student's flow, not a page-level transition.
- **Declined**: a student may skip Challenge Support entirely from the Branching Case Player without penalty — this is optional by design (`FEATURE-BRANCHING-STUDY.md §5` step 9 is marked "[Optional]").

### Boundary
Absolutely no grading, scoring, letter marks, or "correct/incorrect" language in any AI message rendered here (`FR-CS-08`). Not a debate UI — no adversarial "vs." framing, no chat-avatar face, no open-ended free chat after the round cap (`GLOBAL-DESIGN-SYSTEM.md §8`).
