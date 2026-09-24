# P0 — Global Foundation

> **Priority**: NOW. Nothing else can be built consistently without this.
> **Visual system**: `docs/design/GLOBAL-DESIGN-SYSTEM.md` (all tokens/components referenced below live there).
> **Covers**: App shell & role-aware navigation, `/login`, `/register`, case status/mode badges, core component library.

---

## 1. App Shell & Role-Aware Navigation

### Purpose & Function
Provides the persistent frame (sidebar/nav + content area) that every authenticated screen renders inside. Two distinct shells exist — `LecturerLayout` and `StudentLayout` — plus a minimal `PublicLayout` for `/login` and `/register`.

### User & Context
- **Lecturer** sees `LecturerLayout`: full management nav (Courses, Statistics) plus contextual sub-nav once inside a course (Materials, Cases, Review, Feedback).
- **Student** sees `StudentLayout`: a lighter nav, since students mostly deep-link into a specific case from an external LMS/course link rather than browsing a dashboard — case is a required route param on every student route (`SITE.md §5.3`).
- **When used**: On every authenticated screen; this is the persistent frame, not a standalone route.

### Information Hierarchy & Layout
- Sidebar (desktop, 240px fixed) or collapsible drawer (mobile): product wordmark (text only — "CaseTree AI", no logo mark specified), role indicator (small text badge under the wordmark: "Lecturer" / "Student"), primary nav items, user menu (name, sign-out) pinned to the bottom.
- Header bar within content area: page title (`text-display`), optional breadcrumb trail for nested routes (Course → Materials, Course → Cases → Review).
- Content area: `bg-canvas`, centered max-width container on wide screens (avoid full-bleed tables/cards stretching beyond a readable measure on ultra-wide monitors).

### Lecturer Nav Items
- Courses (`/lecturer/courses`) — top-level entry point.
- Statistics (`/lecturer/statistics`) — top-level.
- Contextual, shown only once a course is selected: Materials, Cases (which itself leads to Review and Feedback per case).

### Student Nav Items
Students arrive at a specific case route directly (no course browsing screen in the sitemap). The student shell nav is minimal: current case title/breadcrumb + sign-out. No dashboard/list screen exists in the approved sitemap — do not invent one.

### Actions
- Sign out (clears auth store, routes to `/login`).
- Role-based route guarding (`PrivateRoute` component) — a Student hitting a `/lecturer/*` URL (or vice versa) must be redirected, never shown a broken/empty shell.

### States
- **Loading**: skeleton nav (gray blocks) while auth/profile resolves on first load.
- **Error**: if the session is invalid/expired, redirect to `/login` with a toast: "Your session has expired — please sign in again."

### Responsive Behavior
- Sidebar collapses to a hamburger-triggered drawer under ~768px width.
- Header page title remains visible at all widths; breadcrumbs truncate to the immediate parent only on narrow screens.

### Accessibility
- Nav is a `<nav>` landmark with `aria-label="Main navigation"`.
- Active nav item indicated by both `action-primary` color/underline AND `aria-current="page"` — never color alone.

---

## 2. Login (`/login`)

### Purpose & Function
Authenticates an existing university Lecturer or Student account via email/password (`FEATURE-AUTH-AND-ROLES.md` FR-AUTH-02).

### User & Context
Public/unauthenticated. Entry point for both roles — the same form, role is determined server-side from the account, not selected by the user at login (registration is where role is chosen — see §3).

### Layout
Centered card (max-width ~400px) on `bg-canvas`, vertically centered on the viewport. Wordmark above the card. No sidebar (uses `PublicLayout`).

### Data / Fields
- `email` (required)
- `password` (required)

### Actions
- Submit → `POST /api/v1/auth/login`.
- Link to `/register` ("Don't have an account? Register").

### States
- **Default**: empty form, submit disabled until both fields have content.
- **Loading**: submit button shows a spinner, fields disabled.
- **Error**: generic "Invalid email or password" inline banner (`semantic-error`) — matches `FEATURE-AUTH-AND-ROLES.md` §12 (never reveal which field was wrong, to prevent user enumeration).
- **Success**: redirect to `/lecturer/courses` or the student's case route based on returned `role`.

### Boundary
No social login buttons (Google/Facebook/GitHub) — explicitly out of scope (`FEATURE-AUTH-AND-ROLES.md` §13). No "remember me" / SSO / MFA UI.

---

## 3. Register (`/register`)

### Purpose & Function
Account creation for a new Lecturer or Student (`FEATURE-AUTH-AND-ROLES.md` FR-AUTH-01).

### Layout
Same card pattern as Login.

### Data / Fields
- `email` (required, must be unique)
- `password` (required)
- `fullName` (required)
- `role` — explicit selector, two options only: **Lecturer** / **Student** (segmented control or radio group, not a dropdown — only two mutually exclusive values, per `FEATURE-AUTH-AND-ROLES.md` BR-AUTH-01: one role per account, ever).

### Actions
- Submit → `POST /api/v1/auth/register`.
- Link back to `/login`.

### States
- **Error — duplicate email**: inline banner, "An account with this email already exists."
- **Error — validation**: per-field error text below the offending input (§5.2 of Global Design System).
- **Success**: auto-login and redirect (or redirect to `/login` with a success toast — implementation detail, either is acceptable).

---

## 4. Case Status & Learning-Mode Badges

Not a screen — a shared visual primitive used everywhere a case is listed or referenced (case cards, Case Review header, statistics). Fully specified in `GLOBAL-DESIGN-SYSTEM.md §2.5–2.6, §6.1–6.3`. This entry exists in P0 only to confirm it is a **foundation-priority** deliverable: no other screen (P1–P4) can be built correctly without these badges existing first, since every list/detail screen in the product references case status and/or learning mode.

---

## 5. Core Component Library

The following shared components (fully specified in `GLOBAL-DESIGN-SYSTEM.md §5`) are P0 deliverables, required before any P1+ screen work begins: Button (primary/secondary/destructive), Input, Select, Textarea, Card, Table, Tabs, Badge, Modal, Toast, Empty/Loading/Error states, Confirmation dialog. Build/spec these once, generically, and reuse — do not re-derive per screen.
