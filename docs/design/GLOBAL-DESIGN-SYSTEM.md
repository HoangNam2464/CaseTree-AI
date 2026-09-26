# Edu-Branch-AI — Global Design System

> **Status**: CANONICAL — supersedes `.stitch/DESIGN.md` (retired/deleted).
> **Target Platform**: Google Stitch UI Generation + React 19 / TailwindCSS v4 implementation.
> **Scope**: All Edu-Branch-AI product screens (P0–P4). Does NOT cover the internal "Start Design" tooling — see `SITE.md §7` for its classification.
> **Source of truth**: Product Direction V2 (Edu-Branch-AI), `C1SE_65-CaseTree-AI-Proposal_V1_1.docx`.

---

## 1. Visual Theme & Atmosphere

### 1.1. Core Philosophy
Edu-Branch-AI is a professional academic platform for university lecturers and students. The interface must read as **intellectually rigorous, calm, and content-first** — closer to a well-built academic research/authoring tool than a consumer SaaS product.

- **Theme Mode**: **LIGHT ONLY.** No dark mode in this phase. This is a locked decision (Discovery Plan §P.2) — do not design or generate dark-mode variants.
- **Tone**: Neutral, academic, professional, calm, restrained, natural.
- **AI Representation**: AI is a **function**, never the product's visual identity. No sparkle glyphs as brand signature, no dedicated "AI accent border," no neon/glow, no decorative gradients, no chat-avatar faces, no typing animations. Where AI-originated content must be marked (a Case Draft, a Challenge Support message), use a small, muted, icon + label tag — never a saturated color block. See §2.7 (`ai-support` token).
- **Visual Density**: Medium — generous padding at the page/card level, tightly grouped semantic fields within a card (e.g. a case's status + learning mode + title sit close together).
- **Hierarchy Principle**: Typography (weight/size) leads; color is reserved for status, learning mode, and exactly one primary action per screen. Do not use color as decoration.

### 1.2. What This Replaces
The retired `.stitch/DESIGN.md` specified a near-black theme (`#0d0d10`/`#16161a`) with indigo/violet (`#6366f1`) accents and a sparkle-glyph AI signature, scoped to a single internal tooling screen. **None of those hex values, spacing values, or component specs carry forward.** This document is a from-scratch light-first system covering all 13 product screens.

---

## 2. Color System

All colors are final hex values, locked for Phase 2. Token names are the Tailwind-style names to use in code (`bg-canvas`, `text-primary`, etc.) — see §2.8 for the Tailwind config mapping.

### 2.1. Surface & Background

| Token | Hex | Usage |
|---|---|---|
| `bg-canvas` | `#F9FAFB` | Page background (matches the already-shipped `frontend/src/index.css` base) |
| `bg-surface` | `#FFFFFF` | Cards, panels, modals, table rows |
| `bg-surface-muted` | `#F3F4F6` | Nested blocks, table stripe rows, disabled surfaces, code/quote blocks |
| `bg-surface-hover` | `#F3F4F6` | Hover state for clickable rows/cards on white surface |

### 2.2. Text

| Token | Hex | Usage |
|---|---|---|
| `text-primary` | `#111827` | Headings, primary body text, active input value |
| `text-secondary` | `#4B5563` | Supporting copy, field descriptions, table body text |
| `text-muted` | `#9CA3AF` | Placeholders, timestamps, disabled text, helper captions |
| `text-inverse` | `#FFFFFF` | Text on filled primary-color surfaces (e.g. primary button label) |
| `text-link` | `#2563EB` | Inline links (same hue as `action-primary`), underline on hover |

### 2.3. Borders & Dividers

| Token | Hex | Usage |
|---|---|---|
| `border-default` | `#E5E7EB` | Card borders, input borders, table dividers |
| `border-strong` | `#D1D5DB` | Hover state on interactive card/input borders |
| `border-focus` | `#2563EB` | Focus ring color (see §5.4) |

### 2.4. Primary Accent (`action-primary`)

One restrained accent only — a blue, **not** indigo/violet (that hue is explicitly retired as "AI-coded"). Used for primary buttons, active tab underline, active nav item, links, and focus rings — never repeated decoratively on every card border.

| Token | Hex | Usage |
|---|---|---|
| `action-primary` | `#2563EB` | Default state (buttons, active nav, links) |
| `action-primary-hover` | `#1D4ED8` | Hover |
| `action-primary-active` | `#1E40AF` | Pressed/active |
| `action-primary-disabled` | `#93C5FD` | Disabled primary button background (paired with `text-inverse` at 80% opacity) |
| `action-primary-subtle` | `#EFF6FF` | Light background tint for selected nav items, info banners |

### 2.5. Case Status (case lifecycle: `DRAFT → REVIEWED → APPROVED → PUBLISHED`)

Status color is one of the only two places (with learning mode) where color carries meaning beyond the single accent. Each status is a two-part token: a badge background and a badge text color, always paired (never bare hex on white text without the badge shape).

| Status | Badge BG | Badge Text | Dot/Icon Hex | Meaning |
|---|---|---|---|---|
| `status-draft` | `#F3F4F6` | `#4B5563` | `#9CA3AF` | AI-generated or newly created, not yet human-edited |
| `status-reviewed` | `#EFF6FF` | `#1D4ED8` | `#2563EB` | Lecturer has edited; not yet approved |
| `status-approved` | `#FFFBEB` | `#92400E` | `#D97706` | Lecturer signed off; not yet visible to students |
| `status-published` | `#F0FDF4` | `#166534` | `#16A34A` | Live; visible to students |

### 2.6. Learning Mode (`BRANCHING_STUDY` vs `REVIEW_STUDY`)

The two modes must be visually distinct from each other and from every status color above, and from `action-primary`, so a case card can show status + mode simultaneously without visual collision.

| Token | Badge BG | Badge Text | Meaning |
|---|---|---|---|
| `mode-branching` | `#F0FDFA` | `#0F766E` (teal-700) | Branching Study — decision-tree cases |
| `mode-review` | `#FDF2F8` | `#BE185D` (pink-700) | Review Study — analysis/solution cases |

### 2.7. AI-Origin Marker (`ai-support`)

Used **only** as a small inline tag/icon next to content that originated from AI (a Case Draft before lecturer edit, a Challenge Support message) — never as a page-level theme or button color.

| Token | Hex | Usage |
|---|---|---|
| `ai-support-bg` | `#F3F4F6` | Tag background (same neutral as `bg-surface-muted` — deliberately unsaturated) |
| `ai-support-text` | `#4B5563` | Tag label text, tag icon stroke |

Rendered as a small pill: a plain outline icon (e.g. a generic "document-check" or two-dot icon — never a sparkle/star glyph, never a robot/chat-bubble avatar) + the label text `AI-assisted` or `AI Draft`. Always neutral gray, never colored, never animated.

### 2.8. Semantic Feedback Colors

| Token | Hex | Usage |
|---|---|---|
| `semantic-success` | `#16A34A` | Success toasts, confirmation banners |
| `semantic-warning` | `#D97706` | Warning banners, destructive-adjacent confirmations |
| `semantic-error` | `#DC2626` | Form validation errors, error toasts, destructive button fill |
| `semantic-info` | `#2563EB` | Informational banners (reuses `action-primary` — info is not a competing accent) |

### 2.9. Tailwind Token Mapping (implementation reference)

```
bg-canvas            → bg-[#F9FAFB]
bg-surface           → bg-white
bg-surface-muted     → bg-gray-100   (#F3F4F6)
text-primary         → text-gray-900 (#111827)
text-secondary       → text-gray-600 (#4B5563)
text-muted           → text-gray-400 (#9CA3AF)
border-default       → border-gray-200 (#E5E7EB)
border-strong        → border-gray-300 (#D1D5DB)
action-primary       → bg-blue-600 / text-blue-600 (#2563EB)
action-primary-hover → bg-blue-700 (#1D4ED8)
semantic-error       → text-red-600 / bg-red-600 (#DC2626)
semantic-success     → text-green-600 (#16A34A)
semantic-warning     → text-amber-600 (#D97706)
```
Do not introduce arbitrary hex values outside this table in Stitch prompts or component code — this matches the existing `ui-design-standards.md §3.5` rule.

---

## 3. Typography

System font stack — no custom webfont load (keeps the academic tool feeling fast and utilitarian, not "designed"):

```
font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

| Token | Size / Line-height | Weight | Usage |
|---|---|---|---|
| `text-display` | 28px / 36px | 600 (semibold) | Page-level titles ("Courses", "Case Review") |
| `text-h1` | 24px / 32px | 600 | Section headings within a page |
| `text-h2` | 20px / 28px | 600 | Card/panel titles (case title, node situation label) |
| `text-h3` | 16px / 24px | 600 | Sub-panel labels (form section labels, table group headers) |
| `text-body` | 14px / 20px | 400 | Default body text, form values, table cells |
| `text-body-strong` | 14px / 20px | 500 | Emphasized body text (field labels, active tab) |
| `text-caption` | 12px / 16px | 400 | Timestamps, helper text, badge labels |
| `text-mono` (rare) | 13px / 20px | 400, monospace | IDs shown to lecturers only in dev/debug contexts — never shown to students (§7 security rule) |

Rules:
- Never use color alone to indicate emphasis where weight can do the job (e.g. don't make a label blue to "stand out" — make it `text-body-strong` gray instead).
- Line length for long-form reading content (case situation text, reasoning text, reflection text) should be capped at a readable measure (~65–80 characters) via a `max-w-prose`-equivalent container.

---

## 4. Spacing, Radii, Elevation

### 4.1. Spacing Scale
Follows the existing `ui-design-standards.md` rule — the Tailwind default scale, no arbitrary values:
`4px · 8px · 12px · 16px · 24px · 32px · 48px · 64px`

- Inner card/panel padding: `24px` desktop, `16px` mobile.
- Vertical gap between stacked form sections: `24px`.
- Vertical gap between related fields inside one section: `12px`.
- Horizontal gap between inline badges/tags: `8px`.

### 4.2. Border Radius

| Token | Value | Usage |
|---|---|---|
| `radius-sm` | 6px | Inputs, small buttons, badges (non-pill) |
| `radius-md` | 8px | Buttons, table containers |
| `radius-lg` | 12px | Cards, panels |
| `radius-xl` | 16px | Modals |
| `radius-full` | 9999px | Status/mode badges only (pill shape reserved for badges — NOT for buttons; the retired system's pill-button-as-default is explicitly rejected, Discovery Plan §E) |

### 4.3. Elevation
Minimal, restrained shadows — never a glow/blur decorative effect.

| Token | Value | Usage |
|---|---|---|
| `elevation-0` | none, `border-default` only | Cards on canvas (border does the separation work, not shadow) |
| `elevation-1` | `0 1px 2px rgba(17,24,39,0.05)` | Dropdowns, popovers |
| `elevation-2` | `0 4px 12px rgba(17,24,39,0.10)` | Modals, dialogs |
| `elevation-toast` | `0 4px 16px rgba(17,24,39,0.12)` | Toast notifications |

---

## 5. Shared Component Rules

### 5.1. Button
- **Primary**: `bg action-primary`, `text-inverse`, `radius-md`, height 40px, horizontal padding 16px. One primary button per screen/section — it marks the single main action (e.g. "Publish Case", "Submit Reasoning").
- **Secondary**: `bg-white`, `border-default`, `text-primary`. Used for non-destructive secondary actions ("Cancel", "Save Draft").
- **Destructive**: `bg semantic-error`, `text-inverse`. Reserved for irreversible actions (delete course, delete material) and always paired with a confirmation dialog (§5.10).
- **Disabled**: reduced-opacity fill (`action-primary-disabled`), `cursor-not-allowed`, no hover transform.
- Shape: rectangular with `radius-md`, never a full pill. (Pill shape is reserved for badges only.)

### 5.2. Input / Select / Textarea
- `bg-surface`, `border-default`, `radius-sm`, height 40px (input/select) or min-height 96px (textarea, 4 lines).
- Focus: `border-focus` + 2px ring at 20% opacity of `action-primary`, offset 2px.
- Error state: `border semantic-error`, helper text below in `semantic-error` at `text-caption` size.
- Placeholder: `text-muted`.
- Textareas used for long-form academic writing (student reasoning, reflection, lecturer feedback) should default to a larger min-height (~120–160px) and be resizable vertically.

### 5.3. Card
- `bg-surface`, `border-default`, `radius-lg`, padding 24px (16px mobile), `elevation-0` at rest, `elevation-1` on hover only if the whole card is clickable (e.g. a case list card).

### 5.4. Focus / Interaction States (all interactive elements)
- **Hover**: background shifts to `bg-surface-hover` (for rows/cards) or accent darkens one step (for buttons/links).
- **Active/Pressed**: accent darkens to `-active` token.
- **Focus-visible**: 2px `border-focus` ring, always visible for keyboard navigation — never removed for aesthetics.
- **Disabled**: `text-muted` + reduced opacity (60%) + `cursor-not-allowed`; disabled elements never simply disappear.

### 5.5. Table
- Header row: `bg-surface-muted`, `text-body-strong`, `text-secondary`.
- Body rows: `bg-surface`, alternate striping optional using `bg-surface-muted` at 50% opacity.
- Row hover (if row is clickable): `bg-surface-hover`.
- Dense academic data (statistics, case lists) favors tables over card grids when there are more than ~6 items with 3+ comparable fields.

### 5.6. Tabs
- Underline style, not pill/segmented-control style. Active tab: `text-primary` + 2px `action-primary` underline. Inactive: `text-secondary`, no underline, hover `text-primary`.

### 5.7. Badge / Status Indicator
- `radius-full`, `text-caption`, horizontal padding 8px, vertical padding 2px, always background+text pair from §2.5/§2.6 — never a bare colored dot without a label in a place where status is being communicated as information (a small dot-only variant is acceptable only in dense table cells where a legend is visible elsewhere on screen).

### 5.8. Modal
- Max-width 560px (forms) or 720px (richer content), centered, `radius-xl`, `elevation-2`, `bg-surface`, backdrop `rgba(17,24,39,0.4)` (neutral dark overlay, not black-blur).
- Header: `text-h2` title + close icon (`text-muted`, hover `text-primary`).
- Reserve modals for focused, single-purpose interactions (confirmations, quick edits). Do not wrap primary page content (case review, branching player) in a modal — those are full pages/panels, per Discovery Plan §E ("not everything wrapped in a floating modal").

### 5.9. Toast
- Top-right or bottom-right, `radius-md`, `elevation-toast`, `bg-surface`, left border accent 4px in the relevant semantic color, auto-dismiss ~5s with manual close.

### 5.10. Confirmation Dialog
- Required before any destructive action (delete course/material, unpublish a live case). Modal pattern (§5.8) with a `text-h2` question, one sentence of consequence explained in `text-secondary`, secondary "Cancel" + destructive-styled confirm button.

### 5.11. Empty / Loading / Error States
- **Empty**: centered icon (outline, `text-muted`) + one-sentence `text-secondary` message + primary action if applicable (e.g. "No courses yet" + "Create your first course" button).
- **Loading**: skeleton blocks in `bg-surface-muted` with a subtle pulse — never a spinner-only blank screen for content that has a known shape (tables, cards). A centered spinner is acceptable only for full-page auth transitions.
- **Error**: `semantic-error` icon + plain-language message (never raw server error text/stack traces — matches `ui-design-standards.md §7` security rule) + retry action where applicable.

---

## 6. Product-Specific Components

These are unique to Edu-Branch-AI's domain and must be specified precisely so Stitch does not improvise product behavior.

### 6.1. Case Card
Used in `/lecturer/courses/:courseId/cases` list and course dashboards.
- Shows: title (`text-h2`), learning-mode badge (§2.6), status badge (§2.5), short description (`text-body`, `text-secondary`, 1–2 lines truncated), updated timestamp (`text-caption`, `text-muted`).
- AI-origin marker (§2.7) shown only while status is `status-draft` (i.e. not yet lecturer-touched) — removed once status advances past `DRAFT`, since human-in-the-loop editing has begun.
- Clickable → routes to `/lecturer/cases/:caseId/review`.

### 6.2. Learning-Mode Indicator
Standalone version of the §2.6 badge, used in filters and page headers to indicate which mode a screen/list is scoped to.

### 6.3. Publish/Review Status Stepper
Horizontal 4-step stepper reflecting `DRAFT → REVIEWED → APPROVED → PUBLISHED`. Completed steps: filled `action-primary` connector line + status color dot for that step's own token (§2.5). Current step: outlined, bold label. Future steps: `text-muted`, gray connector. Used at the top of `/lecturer/cases/:caseId/review`.

### 6.4. Decision Node (ReactFlow)
Rectangular card node, `radius-md`, `border-default`, `bg-surface`. Root node gets a small "Start" label chip. Terminal nodes get a distinct visual treatment: `border-strong` + a small flag/checkered icon in `text-muted`, label "Outcome". Non-terminal nodes show a truncated situation preview (`text-body`, 2 lines max) and an option-count badge. Selected/editing node: `border-focus` ring. Never color-code nodes by "correctness" — there is no correct path (Proposal V1.1 guardrail).

### 6.5. Option Selector (Student, Branching Case Player — Experience Phase)
List of 2–4 option cards, each `bg-surface`, `border-default`, `radius-md`, full-width, showing the option text as the primary label. When a student selects an option: the selected option gets `border-focus` highlight, then the player advances **immediately and seamlessly** to the next situation. No reasoning form appears between decision points during the Experience phase. Unselected options are not shown after advancing — the player moves to the next situation node.

### 6.6. REVIEW Phase — Decision Reasoning Input
Large textarea (§5.2 long-form variant) shown in the **REVIEW phase** (after the student has completed their full journey and reached the terminal node) — NOT mid-flow during the Experience phase. In the REVIEW interface, each decision point in the student's path shows: the situation, the option chosen, the alternatives available, and the consequence/outcome (revealed here for the first time). Adjacent to each decision point is an optional reasoning textarea: "Why did you choose this?" / "What would you change?". Label: "Your reasoning" (never "Your argument" — retired term). Helper caption: reflective, plain instruction; no rubric or grading language.

### 6.7. Consequence Display (REVIEW Phase Only)
Revealed in the **REVIEW phase** alongside the reasoning input (§6.6) — **never shown mid-flow during the Experience phase**. Each decision point in the REVIEW timeline shows the consequence of the option the student chose and a brief note on what the alternative(s) would have led to. `bg-surface-muted` panel, `radius-lg`, left border accent in `mode-branching` teal (ties it visually to the Branching Study mode without introducing a new color). Label: "Consequence" (never "Result" or "Outcome" — outcome is reserved for the terminal node's final state per the data model).

### 6.8. Reflection Input
Same visual pattern as Reasoning Input (§6.6), used post-outcome (Branching Study) or post-lecturer-feedback (Review Study). Label: "Your reflection."

### 6.9. Review-Study Submission Card
Shows: case context excerpt, problem text, student's proposed solution, student's reasoning, submission status badge (`SUBMITTED`/`REVIEWED`/`REFLECTED` — reuse the neutral/blue/green progression visually similar to §2.5 but as its own local badge set since this is a different state machine from case status). Used on both the student Review Study screen and the lecturer feedback screen.

### 6.10. Lecturer Feedback Block
`bg-surface-muted` panel distinct from the student's own content blocks, small "Lecturer feedback" label with a person/instructor icon (`text-muted`, never AI-marked — this content is always human-authored per `FEATURE-LECTURER-FEEDBACK.md`).

### 6.11. Challenge Support Panel
Chat-like but **not** a generic chatbot UI: max 2 rounds, each round rendered as a fixed pair (AI counter-question card → optional student response textarea), with a visible round indicator ("Round 1 of 2"). No open-ended input after round 2 — the composer is replaced with a "Session complete" state. AI messages carry the `ai-support` tag (§2.7); they are never styled as a colorful chat bubble — use the same neutral card style as other content, differentiated only by the small AI-origin tag.

### 6.12. Statistics Widgets
Summary number cards (completion rate, attempt count) + a horizontal bar breakdown for branch-selection distribution. Use `action-primary` for the single "current case" data series; do not introduce a rainbow palette for multi-branch breakdowns — use one accent hue at varying opacity steps (100%/70%/40%) instead, keeping with the "one accent" principle (§1.1).

---

## 7. Accessibility Baseline

- All text/background pairs in §2 meet WCAG AA contrast at their intended size (verify `text-muted` on `bg-surface` for caption-sized use only, not body text).
- Every interactive element must have a visible `focus-visible` state (§5.4) — never `outline: none` without a replacement ring.
- Icon-only controls (close buttons, table row actions) require an `aria-label`.
- Form fields require a visible, programmatically associated `<label>` — placeholder text alone is never a substitute for a label.
- Status/mode information must never be conveyed by color alone — always paired with a text label (§2.5, §2.6 badges always carry text).

---

## 8. Explicit Exclusions (do not generate)

- Dark mode / dark theme variants of any screen.
- Indigo/violet (`#6366f1`-family) as an accent, border, or "AI signature" color anywhere.
- Sparkle/star glyphs (`✦` / `✨`) as decorative or brand elements.
- Pill-shaped buttons as a default button style (pills are for badges only).
- Grading marks, score numbers, pass/fail labels, or ranking UI anywhere in the student experience (Proposal V1.1 guardrail — applies to Reasoning, Reflection, and Challenge Support surfaces alike).
- A "debate" framing (chat-bubble avatars, "vs." framing, adversarial styling) for Challenge Support — it is a support panel, not a debate UI.
