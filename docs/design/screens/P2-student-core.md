# P2 — Core Student Flow

> **Priority**: NOW. The other half of the MVP-critical loop.
> **Visual system**: `docs/design/GLOBAL-DESIGN-SYSTEM.md`.
> **Covers**: `/student/cases/:caseId/branching-play`, `/student/cases/:caseId/attempt/:attemptId/reflect`, `/student/cases/:caseId/challenge/:sessionId`.

---

## 1. Branching Case Player (`/student/cases/:caseId/branching-play`)

### Purpose & Function
The core Branching Study interaction loop: Context/Data → Decision Point → Select Option → Student's Own Reasoning per Attempt → Lecturer-authored Consequence → Next Node → Outcome (`FEATURE-BRANCHING-STUDY.md`).

### User & Context
Student only. Requires the case to be `PUBLISHED` (`INV-01`) — non-published cases must 404, not show a locked/preview state (`FEATURE-CASE-REVIEW-AND-PUBLISHING.md §12`).

### Layout
Full-width immersive reading layout (not a dashboard) — this is the "distraction-free decision interface" called for in `SITE.md §2`. Top: case title + a subtle progress indicator (not a percentage bar with false precision — a simple "Decision Point" step marker is enough, since branch length varies). Center: current node's `situation` text in a readable, capped-width column (`GLOBAL-DESIGN-SYSTEM.md §3` line-length rule). Below: Option Selector (`§6.5`). Once an option is picked: Reasoning Input (`§6.6`) appears inline, below the selected option — not a separate page/modal, to keep the decision and its justification visually connected.

### Data
`situation` (current node), list of `CaseOption` (`text`), and — once reasoning is submitted — `consequence` for the chosen option (`GLOBAL-DESIGN-SYSTEM.md §6.7`).

### Flow / States (sequential, matches `FEATURE-BRANCHING-STUDY.md §5` exactly)
1. **Reading**: situation + options shown, no reasoning field yet.
2. **Option selected, reasoning required**: Reasoning Input appears; "Continue" is disabled until reasoning text is non-empty (`FR-BS-03`) — the consequence must not be revealed before reasoning is submitted.
3. **Consequence revealed**: after submit, the Consequence Display renders below the reasoning; an optional prompt to open Challenge Support appears here (see §3 below) — clearly optional, never a forced interstitial.
4. **Advance**: "Continue to Next Situation" button moves to `option.next_node_id`; repeats from step 1.
5. **Terminal reached** (`is_terminal = TRUE`): a distinct Outcome state renders (not just another situation card) — clearly marks this as the end of the path, records `outcome_node_id`, and offers "Reflect on this attempt" → routes to the Reflection screen (§2 below).

### Retry
After reflection (or from a post-outcome summary state), a "Retry Case" action starts a new attempt (`attempt_number + 1`, `FR-BS-09`). Retrying must be visually framed as exploring an alternative path, not as "fixing a wrong answer" — there is no wrong answer (Proposal V1.1 guardrail).

### Boundary
No grading/scoring UI anywhere on this screen. No numeric or letter feedback on the option chosen. No comparison to other students' choices inline (that's a lecturer-only aggregate view — `FEATURE-BASIC-STATISTICS.md`, P3). Consequences are always pre-existing lecturer-authored/approved data returned by the API — never generated live by AI during play (`FEATURE-DECISION-TREE.md §13`: tree is static and pre-approved).

---

## 2. Reflection (`/student/cases/:caseId/attempt/:attemptId/reflect`)

### Purpose & Function
Post-outcome meta-cognitive reflection prompt (`FEATURE-REFLECTION.md`).

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
