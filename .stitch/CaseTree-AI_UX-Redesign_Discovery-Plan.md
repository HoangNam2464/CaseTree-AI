# CaseTree AI — UI/UX Redesign: Phase 1 Discovery + Plan

> **Status**: PLAN ONLY — no project files modified. **Revised** with confirmed decisions below (Section P closed out).
> **Sources used (priority order, as instructed)**:
> 1. `C1SE_65-CaseTree-AI-Proposal_V1_1.docx` (Proposal V1.1) — business/product truth
> 2. `REQUIREMENT-TRACEABILITY.md` + `docs/features/*.md` + `V2__new_flow_schema.sql` — proxy for "Migration Plan Rev 2" (no such file exists standalone; user-confirmed proxy)
> 3. Repository source (`CaseTree-AI_1.zip`, verified identical to GitHub `main` as of this audit)
> 4. `DESIGN.md`, `SITE.md`, `next-prompt.md` (`.stitch/`) — legacy/current UI references, **audited, not authoritative**

---

## A. Current Design Problems

1. **The dark/indigo/sparkle aesthetic exists only in design documents, not in code.** `frontend/src/index.css` and `tailwind.config.js` currently ship a plain **light** theme (`#f9fafb` background, `#2563eb` blue primary, no indigo, no dark mode). `DESIGN.md` / `next-prompt.md` describe a near-black (`#0d0d10`/`#16161a`) theme with indigo/violet (`#6366f1`) accents and a sparkle glyph (`✦`) as the AI signature. These two are unrelated — the dark/AI-glyph direction was authored for one Stitch prompt and never implemented. **This is good news**: there is no dark theme to "undo" in real code, only in documents that would otherwise keep generating more dark/indigo screens if reused as-is.
2. **The existing design system is scoped to exactly one screen** (the "Bắt đầu với thiết kế của bạn" / Start Design modal) and provides no rules for the other 12 routes (courses, materials, cases, case review, statistics, lecturer feedback, branching player, reflection, review study, review feedback, challenge support, login/register).
3. **AI is currently treated as the product's visual identity**, not a feature: sparkle glyph (`✦`) on the primary button, a dedicated signature indigo border reserved for the one AI-related textarea, "XEM TRƯỚC" AI badge styling. Proposal V1.1 explicitly frames AI as an assistive, human-in-the-loop function (case drafting, challenge questions) — never the product's headline identity.
4. **No semantic status/workflow color system exists**, despite the product being built entirely around statuses: case lifecycle (`DRAFT → REVIEWED → APPROVED → PUBLISHED`), two learning modes (`BRANCHING_STUDY` / `REVIEW_STUDY`), and review-study submission states (`SUBMITTED → REVIEWED → REFLECTED`). None of this is represented in `DESIGN.md`'s color table.
5. **No component system** beyond one modal's inputs/cards/button — no defined Table, Tabs, Badge-as-status, Empty/Loading/Error state, or the product-specific components (case card, decision node, consequence display, reasoning input, lecturer feedback block) that the actual product needs.

## B. Product / UI Inconsistencies (Conflicts Found)

| # | Conflict | Evidence | Recommendation |
|---|---|---|---|
| 1 | **Legacy rule files describe a forbidden "AI Debate Assistant / Devil's Advocate"** | `.agents/rules/feature-debate-assistant.md` (keywords include "devil advocate"), `.agents/rules/feature-argument.md`, `.agents/rules/feature-simulator.md` — all reference `debate/`, `argument/`, `simulation/` backend modules that **no longer exist** in the repo (replaced by `challenge-support/`, `reasoning/`, `branching-attempt/`). Proposal V1.1 explicitly states (lines 38, 62): AI Reasoning/Challenge Support "does not grade, score or decide academic right or wrong, and **it is not a debate platform**." | **DELETE** `feature-debate-assistant.md`. **REPLACE** with a new rule file describing `challenge-support/` (2-round Socratic counter-questions, no grading) sourced from `docs/features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`. **UPDATE** `feature-argument.md` → rename concept to "reasoning" (`reasoning/` module), matching `docs/features/FEATURE-BRANCHING-STUDY.md`. **UPDATE** `feature-simulator.md` → rename to `branching-attempt/` terminology, matching `docs/features/FEATURE-BRANCHING-ATTEMPT.md`. *(Flagged only — not modified.)* |
| 2 | **`.agents/rules/ui-design-standards.md` §5 lists stale, incomplete routes** | Lists `/student/cases/:caseId/simulate` and `/student/cases/:caseId/debate/:sessionId` — neither exists in `router.tsx`. Missing entirely: `review-study`, `review-study/:submissionId/feedback`, `cases/:caseId/feedback` (lecturer feedback), `attempt/:attemptId/reflect`. | **UPDATE** §5 to mirror the live `router.tsx` route list (given in Section C below). |
| 3 | **`SITE.md` describes a "Debate Assistant" acting as a "Socratic Devil's Advocate"** | Section 1 (Product Vision) of `SITE.md`. Directly contradicts Proposal V1.1's explicit "not a debate platform" statement. | Confirms `SITE.md` is legacy/non-authoritative, as already instructed. Not used as a requirement source. No action needed on the file itself (out of scope — it's a reference doc, not a rule file the AI agent executes against). |
| 4 | **The "Start Design" modal (`DESIGN.md`/`next-prompt.md`/`SITE.md §7`) does not correspond to any screen in Proposal V1.1, `REQUIREMENT-TRACEABILITY.md`, or the live `router.tsx`.** | `SITE.md` claims a public route `/start-design` (or `/design`); no such route exists in `frontend/src/app/router.tsx` (verified against both the zip and live GitHub `main`). Proposal V1.1 never describes lecturers/students supplying their own `DESIGN.md`, Figma files, or brand assets. | **Needs your confirmation (see Section P).** Best guess without inventing: this modal is very likely a **meta-tool for generating CaseTree AI's own UI via Stitch** (i.e., tooling for *you*, not a feature of the shipped product for lecturers/students). If that's correct, it should **not** be treated as a product screen in the new design system at all — it's a Stitch-prompting artifact, separate from the actual app. I have not assumed this; flagged for your decision. |
| 5 | **Router comment claims a "Final Migration Plan Rev 2" as source of truth** | `frontend/src/app/router.tsx` line 3. No such file exists anywhere in the repository. | Resolved per your instruction: `REQUIREMENT-TRACEABILITY.md` + `docs/features/*.md` + `V2__new_flow_schema.sql` serve as the proxy. Comment is stale but out of scope to edit during a design-only audit. |

## C. Product Screen Inventory

All 13 routes below are **ACTUAL** (exist in `router.tsx`, verified identical on both the audited zip and GitHub `main`) and **DOCUMENTED** (each maps to a `docs/features/*.md` file and a `REQUIREMENT-TRACEABILITY.md` row). **Current implementation status for every single one: placeholder stub only** (a heading + one sentence of gray text, e.g. `CaseReviewPage.tsx`, `BranchingCasePlayerPage.tsx` — confirmed by direct inspection). This is a genuine greenfield UI build, not a re-skin.

| Screen | Role | Purpose | Learning Mode | Workflow Position | Status | 
|---|---|---|---|---|---|
| `/login` | Public | Sign in | — | Entry | Scaffolded |
| `/register` | Public | Account creation | — | Entry | Scaffolded |
| `/lecturer/courses` | Lecturer | Course catalog & creation | Both | Start | Scaffolded |
| `/lecturer/courses/:id/materials` | Lecturer | Upload/inspect teaching material (PDF/DOCX), RAG chunk status | Both | Pre-generation | Scaffolded |
| `/lecturer/courses/:id/cases` | Lecturer | Case list, filter by learning mode, trigger AI generation | Both | Generation trigger | Scaffolded |
| `/lecturer/cases/:id/review` | Lecturer | Verify/edit/approve/publish Case Draft (ReactFlow tree editor for Branching; form editor for Review) | Both | Human-in-the-loop gate | Scaffolded |
| `/lecturer/cases/:id/feedback` | Lecturer | Review student Review-Study submissions, write feedback | Review Study only | Post-submission | Scaffolded |
| `/lecturer/statistics` | Lecturer | Completion, branch distribution, attempts, outcome | Branching (primarily) | Ongoing | Scaffolded |
| `/student/cases/:id/branching-play` | Student | Context → Decision Point → Option → Reasoning → Consequence → Next Node → Outcome | Branching Study | Core loop | Scaffolded |
| `/student/cases/:id/attempt/:attemptId/reflect` | Student | Post-outcome reflection; entry point to retry | Branching Study | After outcome | Scaffolded |
| `/student/cases/:id/challenge/:sessionId` | Student | AI Reasoning/Challenge Support, max 2 rounds, counter-questions only | Both | Optional, mid-flow | Scaffolded |
| `/student/cases/:id/review-study` | Student | Context/data/problem → analysis → proposed solution + reasoning | Review Study | Core loop | Scaffolded |
| `/student/cases/:id/review-study/:submissionId/feedback` | Student | View lecturer feedback, reflect | Review Study | After lecturer review | Scaffolded |

Not a screen, but a required **shared state, not a route**: **Case Draft verify/edit/approve** is the single most business-critical interaction in the product (Proposal V1.1, Objective 2 & Deliverable 1) and lives inside `/lecturer/cases/:id/review` — it deserves the deepest component work of anything in this system.

## D. Screen Priorities

| Priority | Screens | Rationale |
|---|---|---|
| **P0 — Global foundation** | App shell, Sidebar/Nav (Lecturer + Student layouts), Login, Register, Case status badges, core component library (button/input/card/table/tabs/badge/modal/toast/empty/loading/error) | Nothing else can be built consistently without this |
| **P1 — Core lecturer flow** | Courses, Materials, Cases list, **Case Review (Branching Study editor)** | Proposal V1.1 frames Branching Study as "the fully developed flow and focus of the MVP" — this is the critical path |
| **P2 — Core student flow** | Branching Case Player, Reflection, Challenge Support | The other half of the MVP-critical loop |
| **P3 — Support/statistics** | Lecturer Statistics, Lecturer Feedback (Review Study) | Important but not blocking the MVP classroom trial (which is Branching-Study-focused per Proposal V1.1 line 52, 65) |
| **P4 — Secondary states/details** | Review Study (student), Review Feedback (student) | Proposal V1.1 explicitly calls Review Study "supported at a simple level in the MVP" — lowest build priority by the product owner's own words |

Per-screen sequencing is confirmed (Section P.3):
- **NOW**: **P0** Global Foundation, **P1** Core Lecturer Flow, **P2** Core Student Flow.
- **LATER**: **P3** Statistics & Lecturer Feedback, **P4** Review Study & Review Feedback.
- **NOT NEEDED YET**: Start Design (confirmed as internal tooling only, excluded from the product screen inventory).

## E. Proposed New Visual Direction

**Principle**: AI is a *function* (a labeled action, a small icon next to a specific button/panel), never the *skin* of the product. Remove: sparkle glyphs as brand signature, dedicated "AI accent border," neon/glow, gradients used decoratively, pill-shaped buttons as a universal default (fine for one modal, reads as consumer-SaaS everywhere else).

**Confirmed theme — LIGHT (locked per Section P.2)**: Proposal V1.1 does not specify a theme, and the actual shipped code defaults to **light**. The product owner has confirmed a **light-first, neutral-gray academic UI** (clean, calm readability, professional presentation, content-first design) as the sole default identity. Dark mode is **not** supported this phase, and the legacy dark/indigo palette is fully retired.

**Target qualities restated concretely**:
- Typography-led hierarchy over color-led hierarchy (weight/size do the work; color reserved for status and one primary action per screen)
- One accent color used sparingly for primary actions and links — not repeated on every card/border
- Status color (case lifecycle, learning mode) is the *only* place color carries meaning beyond the single accent
- Dense, readable data surfaces (tables for statistics, structured cards for cases) — not everything wrapped in a floating modal

## F. Proposed New Color System (direction, not final hex — to be locked in Phase 2)

| Token | Purpose | Direction |
|---|---|---|
| `bg-canvas` | Page background | Off-white / very light neutral gray |
| `bg-surface` | Cards, panels | White |
| `bg-surface-muted` | Nested blocks, table stripes | Light gray |
| `text-primary` / `text-secondary` / `text-muted` | Content hierarchy | Neutral gray scale, no tint |
| `border-default` | Structural lines | Light neutral gray |
| `action-primary` | One accent, primary buttons/links | A single restrained blue or teal (not indigo/violet — avoid AI-coded hue) |
| `status-draft` | Case status: DRAFT | Neutral gray |
| `status-approved` | Case status: APPROVED | Amber/gold (in-progress, not yet live) |
| `status-published` | Case status: PUBLISHED | Green |
| `mode-branching` | Learning-mode tag: Branching Study | Accent A |
| `mode-review` | Learning-mode tag: Review Study | Accent B (distinct, not a shade of A) |
| `ai-support` | AI-origin content marker (Case Draft, Challenge Support) | Small, muted, icon-based — not a saturated color block |
| `semantic success/warning/error/info` | Standard feedback | Standard semantic greens/ambers/reds/blues |

Exact hex values, full interactive-state table, and full typography scale belong in Phase 2 (`Global Design System` doc) once direction is approved — producing final hex now would be guessing ahead of your sign-off on light-vs-dark.

## G. Component Architecture (to be built in Phase 2)

**Foundational** (shared across all screens): App shell, Sidebar (role-aware: Lecturer/Student), Header, Button (primary/secondary/destructive), Input, Select, Textarea, Card, Table, Tabs, Badge, Status indicator, Modal, Toast, Empty state, Loading state, Error state, Confirmation dialog.

**Product-specific**: Case card (shows learning mode + status), Learning-mode indicator (Branching/Review tag), Decision node (ReactFlow node for tree editor/player), Option selector, Consequence display, Reasoning input, Reflection input, Review-study submission card, Lecturer feedback block, Challenge Support panel (round 1/2 indicator), Statistics widgets (completion, branch distribution), Publish/review status stepper (`DRAFT → REVIEWED → APPROVED → PUBLISHED`).

## H. Reference Strategy

No external references have been evaluated yet in this pass — Phase 1 was scoped to internal audit. Recommendation for Phase 2: pull 2–3 concrete references only where they solve a named problem (e.g., a status-stepper pattern for the case lifecycle, a decision-tree canvas pattern for ReactFlow editing), each logged as `SOURCE / OBSERVATION / RECOMMENDATION`, never as a branding template to copy.

## I. Stitch Rules (generalized beyond one screen)

Every future Stitch prompt for any CaseTree AI screen must state: **WHAT** screen, **WHO** uses it (Lecturer/Student), **WHY** (which Proposal V1.1 objective it serves), **WHEN** (workflow position), **DATA** (fields that must appear, sourced from `docs/features/*.md`), **ACTION** (only actions in the traceability matrix), **STATE** (loading/empty/error/disabled/success), **VISUAL** (the new light-first system, not the retired dark/indigo palette), **BOUNDARY** (explicitly: no Debate Assistant, no grading/scoring UI, no ranking/comparison UI, no Review Study retry UI — all excluded per Proposal V1.1).

## J. Recommended Documentation Structure

| Document | Purpose | Replaces |
|---|---|---|
| `GLOBAL-DESIGN-SYSTEM.md` | Colors, type, spacing, component rules (Phase 2 output of Sections E–G above) | `DESIGN.md` |
| `SCREEN-SPECIFICATIONS.md` (or one file per P0–P4 batch) | Per-screen spec using the 10-section template from your original prompt | *(new)* |
| `STITCH-GENERATION-GUIDELINES.md` | The WHAT/WHO/WHY/... rules generalized (Section I above) | Supersedes retired Stitch prompt references |
| Keep `SITE.md`'s **sitemap/workflow diagrams** (Sections 5–6) as **architecture reference only**, after removing the Debate-Assistant language in Section 1 | Product vision framing (Section 1) is superseded by Proposal V1.1; sitemap is still accurate | — |

## K. Migration Strategy from Old Design Docs

1. Do not carry forward any hex value, spacing value, or component spec from `DESIGN.md`/`next-prompt.md` as-is — they were built for one screen under an aesthetic direction you've now rejected.
2. Extract only the *structurally reusable* patterns worth keeping conceptually (e.g., modal max-width discipline, disabled/active button state logic, drag-and-drop card pattern) and re-skin them under the new light/neutral system.
3. Treat `SITE.md` Sections 2–6 (roles, goals, sitemap, workflows) as accurate architecture reference; discard Section 1's "Debate Assistant" framing and Section 8's "Dark-Themed Elegance" framing (superseded by Section E above and confirmed in Section P.2).

## L. Files to Create (Phase 2, after your approval)
- `docs/design/GLOBAL-DESIGN-SYSTEM.md`
- `docs/design/STITCH-GENERATION-GUIDELINES.md`
- `docs/design/screens/P0-foundation.md`, `P1-lecturer-core.md`, `P2-student-core.md`, `P3-support.md`, `P4-review-study.md`

## M. Files to Rewrite / Status of Legacy Docs
- `.agents/rules/ui-design-standards.md` §5 (route list correction)
- *(Note on retired Stitch docs: `.stitch/DESIGN.md` and `.stitch/next-prompt.md` are permanently retired and deleted; they do NOT need to be rewritten, recreated, or maintained in Phase 2. All canonical design specs reside in `docs/design/`).*

## N. Files to Delete (proposed — not executed)
- `.agents/rules/feature-debate-assistant.md`

## O. Files to Preserve As-Is
- `docs/C1SE_65-CaseTree-AI-Proposal_V1_1.docx`
- `docs/requirements/REQUIREMENT-TRACEABILITY.md`
- `docs/features/*.md` (all current, matching live modules)
- `infrastructure/postgres/migrations/V2__new_flow_schema.sql`
- `SITE.md` Sections 2–7 (sitemap/roles/workflows), as architecture reference

## P. Clarifications — RESOLVED (confirmed by product owner)

1. **"Start Design" modal → INTERNAL TOOLING, not a product screen.**
   Confirmed: `DESIGN.md` / `next-prompt.md` (`.stitch/`) are internal Stitch/UI-authoring references, not a CaseTree AI feature, and have been retired/deleted. Effective immediately:
   - Removed from the product screen inventory (Section C already excluded it — no change needed there).
   - It will **not** be designed as a lecturer/student screen in this system.
   - `SITE.md §7` is strictly classified as **INTERNAL DESIGN TOOLING ONLY**, not product scope.
   - `next-prompt.md` and `DESIGN.md` are retired/deleted; Phase 2 will not recreate or rewrite them.

2. **Theme → LIGHT, confirmed as default. No dark mode this phase.**
   Section E/F direction is now locked: light-first, neutral, academic, professional. The dark/indigo palette from `DESIGN.md` is fully retired, not preserved as an alternate mode.

3. **Screen sequencing → confirmed:**
   - **NOW**: P0 Global Foundation, P1 Lecturer Core, P2 Student Core
   - **LATER**: P3 Statistics / Lecturer Feedback, P4 Review Study / Review Feedback (still in scope for the product — later implementation order only, not removed)
   - **NOT NEEDED YET**: Start Design (confirmed not a product screen at all, per #1)

4. **Legacy `.agents/rules/*` — approved to modify in Phase 2:**
   - `feature-debate-assistant.md` → **DELETE**, replaced by a new Challenge Support rule file (sourced from `docs/features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`)
   - `feature-argument.md` → **UPDATE/RENAME** to Reasoning terminology (`reasoning/` module)
   - `feature-simulator.md` → **UPDATE/RENAME** to Branching Attempt / Branching Study terminology (`branching-attempt/` module)
   - `ui-design-standards.md` §5 → **UPDATE**, replace stale route list with the actual `router.tsx` routes (Section C table above)

5. **`SITE.md` — additional legacy terminology found on re-check (beyond §1 and §7), to be corrected when `SITE.md` is next touched:**

   | Line | Current text | Issue | Fix direction |
   |---|---|---|---|
   | 14 (§1) | "A built-in AI Debate Assistant acts as a Socratic 'Devil's Advocate'..." | Contradicts Proposal V1.1 "not a debate platform" | Rewrite using Challenge Support / Reasoning language |
   | 27 (§2, Student role) | "...engages in up to 2 rounds of Socratic debate with the AI assistant..." / "...interactive debate cards" | "debate" framing | → "up to 2 rounds of AI Challenge Support" / "challenge-question cards" |
   | 37 (§3, Goal 3) | "Socratic Reasoning Challenge, NOT Autonomous Grading" — uses "student arguments" | Minor terminology drift (not a hard conflict; concept is accurate) | → "student reasoning" |
   | 47 (§4, Product Experience) | "**Dark-Themed Elegance**: ...dark surfaces...to reduce visual fatigue..." | Contradicts confirmed **light** theme decision | Replace with a light-theme attribute (e.g. "Clear, Calm Readability") |
   | 65 (§5.2 sitemap) | "Review student **arguments**" | Terminology drift | → "Review student reasoning/submissions" |
   | 69 (§5.3 sitemap) | "Branching Decision Tree **Simulator**" | Old module name (`simulation/` → `branching-attempt/`) | → "Branching Case Player" (matches Proposal V1.1 line 34, 58) |
   | 89 (§6, Workflow 4 title) | "Workflow 4: Student **Simulation**" | Old terminology | → "Workflow 4: Branching Study Playthrough" |
   | 116–117 (§8, Design Roadmap) | "...adopting the **dark academic design system**" / "...with **dark** distraction-free presentation" / "Student Decision **Simulator**" | Contradicts light-theme decision + old terminology | Replace with light-system wording; rename Simulator → Branching Case Player |

   *(Note: Audited and resolved — `SITE.md` has been updated to the light-first theme, accurate architecture, and proper P0–P4 roadmap).*

---

## Phase 2 — Execution Plan (awaiting your go-ahead to start)

Scope: **documentation and rule-file changes only** — no application code, no `frontend/src` changes (all pages remain the placeholder stubs they are today; this phase produces the design *spec* they'll be built from later).

| Step | Action | Output file(s) | Type |
|---|---|---|---|
| 1 | Write the full light-theme color system (final hex, semantic tokens, interactive states) | `docs/design/GLOBAL-DESIGN-SYSTEM.md` | CREATE |
| 2 | Write typography, spacing, elevation, and the full shared + product-specific component rules (Sections F–G expanded to full spec) | *(same file, or split if it gets long — will confirm)* | CREATE |
| 3 | Write generalized Stitch generation guidelines (WHAT/WHO/WHY/WHEN/DATA/ACTION/STATE/VISUAL/REFERENCE/BOUNDARY) | `docs/design/STITCH-GENERATION-GUIDELINES.md` | CREATE |
| 4 | Write per-priority screen specs, starting with P0+P1 (NOW), using the 10-field template (purpose, entry/exit, states, acceptance criteria, etc.) | `docs/design/screens/P0-foundation.md`, `P1-lecturer-core.md` | CREATE |
| 5 | Write P2 (NOW) screen specs | `docs/design/screens/P2-student-core.md` | CREATE |
| 6 | Write P3/P4 (LATER) screen specs — lighter pass, since they're not immediate build targets | `docs/design/screens/P3-support.md`, `P4-review-study.md` | CREATE |
| 7 | Confirm retirement of legacy Stitch docs | `.stitch/DESIGN.md`, `.stitch/next-prompt.md` | RETIRED/DELETED (no rewrite needed; canonical docs live in `docs/design/`) |
| 8 | Delete/replace debate-assistant rule | `.agents/rules/feature-debate-assistant.md` | DELETE + new `feature-challenge-support.md` (CREATE) |
| 9 | Rename/update argument rule | `.agents/rules/feature-argument.md` → `feature-reasoning.md` | RENAME + UPDATE |
| 10 | Rename/update simulator rule | `.agents/rules/feature-simulator.md` → `feature-branching-attempt.md` | RENAME + UPDATE |
| 11 | Fix stale routes and theme framing | `.agents/rules/ui-design-standards.md` | UPDATE |
| 12 | Apply terminology/theme corrections table (Section P.5) | `SITE.md` | COMPLETED (audited and updated to light-first & P0–P4 roadmap) |

**Not in Phase 2 scope** (flagging so it isn't assumed later): no `frontend/src` component code, no Tailwind config changes, no actual React implementation — this phase is documentation/specification only, matching the "STRUCTURAL SKELETON ONLY" state of the real codebase.

**Still open, not blocking Phase 2 start, but will need a decision before Step 1 locks final hex values:** none — theme, priorities, and scope are all confirmed. Phase 2 can begin as soon as you confirm the step order/grouping above (e.g., whether you want one combined `GLOBAL-DESIGN-SYSTEM.md` or split files, and whether to do all steps in one pass or prioritize NOW-priority steps 1–5+8–11 and defer step 6 details).

---

**Waiting for your go-ahead to execute Phase 2.**
