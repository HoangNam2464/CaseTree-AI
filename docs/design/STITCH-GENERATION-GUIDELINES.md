# Edu-Branch-AI — Stitch Generation Guidelines

> **Status**: CANONICAL — supersedes the single-screen prompt conventions in the retired `.stitch/next-prompt.md`.
> **Purpose**: Every Stitch prompt written for any Edu-Branch-AI screen (P0–P4) must be assembled using the nine fields below, in order. This keeps generation grounded in approved product behavior instead of improvising UI or functionality.
> **Source**: `CaseTree-AI_UX-Redesign_Discovery-Plan.md` §I, generalized from one screen to the full product.

---

## 1. The Nine Fields

Every prompt states all nine. If a field is genuinely not applicable to a given screen, write "N/A — [reason]" rather than omitting it silently, so the omission is traceable.

### WHAT
The exact screen or component being generated, named using **current terminology only** (see §3). State the route it corresponds to (from `SITE.md §5`) if it's a full screen, or the parent screen it belongs to if it's a sub-component.

### WHO
Which role uses it: **Lecturer** or **Student** (never both with identical content — even shared concepts like Challenge Support render differently per role's data). Reference the role table in `SITE.md §2`.

### WHY
Which product objective it serves, traced to Proposal V1.1's stated goals (active decision-making, human-in-the-loop AI governance, Socratic reasoning challenge without grading, pedagogical insight — `SITE.md §3`). A screen with no traceable objective should not be generated.

### WHEN
Its position in the workflow — reference the relevant workflow diagram in `SITE.md §6` (Material Ingestion / Case Generation / Human-in-the-Loop Review / Branching Study / Review Study / Challenge Support). State what precedes and what follows this screen.

### DATA
The exact fields that must appear, sourced from the corresponding `docs/features/FEATURE-*.md` file's "Data Involved" section — never invented. List field names as they exist in the data model (e.g. `reasoning_text`, not "the student's answer").

### ACTION
Only the actions defined in `docs/requirements/REQUIREMENT-TRACEABILITY.md` / the feature doc's Functional Requirements. If an action is not in a feature doc, it does not belong in the prompt.

### STATE
Every state the screen must handle: `loading`, `empty`, `error`, `disabled`, `success`, and any domain-specific state (e.g. "session complete" for Challenge Support after round 2, "read-only" for a student viewing a non-owned attempt). Reference `GLOBAL-DESIGN-SYSTEM.md §5.11` for the shared empty/loading/error patterns.

### VISUAL
The light-first system only — reference `GLOBAL-DESIGN-SYSTEM.md` token names directly (e.g. `bg-canvas`, `action-primary`, `status-published`). Never restate raw hex from memory; pull from the tables in that document so values stay single-sourced. Never reference the retired dark/indigo palette, even as a "before" comparison inside a prompt.

### REFERENCE
Zero to three external references, only where they solve a **named, specific problem** (e.g. a status-stepper interaction pattern, a decision-tree canvas pattern), logged as:
```
SOURCE: <where it's from>
OBSERVATION: <the specific pattern being referenced>
RECOMMENDATION: <how it applies here, re-skinned to our tokens>
```
Never used as a branding template to copy wholesale. Omit this field entirely if no reference is needed — do not force one.

### BOUNDARY
Explicit exclusions for this screen, drawn from the relevant feature doc's "Excluded" / "Out of Scope" / guardrail sections, plus the standing product-wide boundaries that apply everywhere:
- No Debate Assistant framing (chat-vs-AI, adversarial styling) — it is Challenge Support.
- No grading, scoring, ranking, or pass/fail UI anywhere in the student experience.
- No Review Study retry/resubmission UI (one submission per student per case — `FEATURE-REVIEW-STUDY.md` §3).
- No dynamic AI-invented runtime outcomes in Branching Study — consequences are always lecturer-authored/approved, pre-existing data, never generated live during play.
- No dark mode.

---

## 2. Prompt Template

```
# Stitch Prompt: <Screen Name> (<route>)

## WHAT
<screen/component, route>

## WHO
<Lecturer | Student> — <one line on this role's relationship to the screen>

## WHY
<Proposal V1.1 objective this serves>

## WHEN
<workflow position: precedes / follows>

## DATA
- <field_name>: <type/source>
- ...

## ACTION
- <action>: <what it does, which endpoint/flow it triggers per the feature doc>
- ...

## STATE
- loading: <what renders>
- empty: <what renders>
- error: <what renders>
- <domain-specific state>: <what renders>

## VISUAL
Reference: GLOBAL-DESIGN-SYSTEM.md
- Surfaces: <tokens>
- Accent usage: <tokens>
- Status/mode badges present: <yes/no, which>

## REFERENCE (optional)
SOURCE / OBSERVATION / RECOMMENDATION — or omit this section entirely.

## BOUNDARY
- <explicit exclusion 1>
- <explicit exclusion 2>
- (always include the standing product-wide boundaries from §1 BOUNDARY above)
```

---

## 3. Current Terminology (mandatory — do not use retired terms in any prompt)

| Use this | Never this |
|---|---|
| Student Reasoning / Reasoning | Argument, Student Argument |
| AI Reasoning / Challenge Support | Debate Assistant, Devil's Advocate |
| Branching Study | — (product name, unchanged) |
| Branching Case Player / Branching Attempt | Simulator, Simulation |
| Review Study | — (product name, unchanged) |
| Lecturer Feedback | — (product name, unchanged) |
| Consequence (revealed after reasoning) | Result |
| Outcome (terminal node's final state) | Ending, Result |
| Counter-question / Challenge question | Debate question |

The internal "Start Design" tooling screen (`SITE.md §7`) is never a subject of a product-screen Stitch prompt — it is developer tooling, out of the product screen inventory entirely.

---

## 4. Screen Index

Prompts should be written per the priority grouping already established in `docs/design/screens/`:
- `P0-foundation.md` — app shell, nav, auth, core component library
- `P1-lecturer-core.md` — courses, materials, cases list, Case Review
- `P2-student-core.md` — Branching Case Player, Reflection, Challenge Support
- `P3-support.md` — Statistics, Lecturer Feedback
- `P4-review-study.md` — Review Study, Review Feedback

Each screen file provides the WHAT/WHO/WHY/WHEN/DATA/ACTION/STATE content pre-filled from its feature doc; a Stitch operator fills in VISUAL/REFERENCE/BOUNDARY per this guide when actually generating.
