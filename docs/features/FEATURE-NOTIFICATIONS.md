# Feature: Deadline & Case Notification System

> **Authoritative Traceability**: Item 27 (Proposal Section 4 p. 7)  
> **Target Package / Module**: Backend `notification/` (Future Extension Boundary)  
> **Delivery Channel Options**: Kept strictly at Proposal-level options (**`In-App`**, **`Email`**, **`Hybrid`**). Implementation technologies (WebSocket, polling, SMTP, SendGrid) are unselected pending Project Owner decision.

---

## 1. Purpose
Provides targeted educational reminders to university students to complete assigned interactive branching case studies before a designated deadline, ensuring timely participation in case simulations and debate sessions.

---

## 2. Actors
- **Lecturer**: Assigns a published case study with an optional completion deadline.
- **Student**: Receives reminders about upcoming or pending case study assignments.
- **System**: Evaluates deadlines and triggers notification events.

---

## 3. Scope
- Defining assignment deadlines for published cases.
- Generating reminder events before deadlines (e.g. 24 hours prior).
- Documenting candidate delivery channels (**In-App**, **Email**, **Hybrid**).
- Maintaining notification delivery status (sent, read, pending).

---

## 4. Functional Requirements
- **FR-NOTIF-01**: The system shall allow a lecturer to set an optional deadline (`due_date`) when publishing or assigning a case study to a course cohort.
- **FR-NOTIF-02**: The system shall generate reminder notifications for enrolled students who have not completed the assigned case study prior to the deadline.
- **FR-NOTIF-03**: The system architecture shall support Proposal-level delivery options:
  - **Option A (In-App)**: Notifications visible when the student logs into the EduBranch AI web application.
  - **Option B (Email)**: Direct notification sent to the student's registered university email address.
  - **Option C (Hybrid)**: In-app notification with an optional email reminder closer to the deadline.
- **FR-NOTIF-04**: The system shall allow students to dismiss or mark notifications as read.

---

## 5. Main Flow
1. Lecturer publishes a case and sets a completion deadline (e.g., Friday at 23:59).
2. The notification scheduler evaluates pending simulation sessions.
3. Students who have not completed the session receive a reminder notification via the approved delivery channel.
4. Student clicks the reminder link, taking them directly to `/student/cases/:caseId/simulate`.
5. Upon session completion, subsequent reminders for that case are automatically suppressed.

---

## 6. Inputs
- Case Assignment Deadline: `caseId` (UUID), `dueDate` (TIMESTAMPTZ).
- Notification Preference (Future): Student notification opt-ins/opt-outs.

---

## 7. Outputs
- Notification Record: `{ id, studentId, title, message, caseId, dueDate, status, createdAt }`.
- Delivery Event: In-app badge/message or transactional email dispatch.

---

## 8. Business Rules
- **BR-NOTIF-01**: Notifications must only be sent for cases in `PUBLISHED` status.
- **BR-NOTIF-02**: Students who have already completed the simulation session (`is_completed = TRUE`) must NOT receive reminder notifications.
- **BR-NOTIF-03**: The notification system must never send promotional or non-academic messages; it is strictly limited to case deadline reminders.
- **BR-NOTIF-04**: No specific delivery technology (such as WebSockets, SendGrid, or polling) is assumed at this stage; implementation will follow Project Owner approval.

---

## 9. Permissions
- Role `LECTURER`: Can configure assignment deadlines for owned courses.
- Role `STUDENT`: Can view and dismiss their own notifications.

---

## 10. Dependencies
- Course and Case domain entities.
- Relational database storage for notification records.
- Delivery provider (to be decided by Project Owner).

---

## 11. Data Involved
- Future Conceptual Schema:
  - `id`: UUID (PK)
  - `user_id`: UUID REFERENCES users(id)
  - `case_id`: UUID REFERENCES cases(id)
  - `type`: VARCHAR(50) (e.g., `CASE_ASSIGNED`, `DEADLINE_REMINDER`)
  - `channel`: VARCHAR(50) (`IN_APP`, `EMAIL`)
  - `is_read`: BOOLEAN DEFAULT FALSE
  - `sent_at`: TIMESTAMPTZ

---

## 12. Error / Edge Cases
- Student without valid email: Suppress email dispatch; fall back to in-app notification.
- Case deadline changed or cancelled: Invalidate or cancel pending unsent reminder tasks.

---

## 13. Out of Scope
- Real-time peer-to-peer chat messaging between students.
- SMS or mobile push notifications.
- Marketing broadcast announcements.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Item 27)
- [`docs/architecture/SERVICE-BOUNDARIES.md`](../architecture/SERVICE-BOUNDARIES.md)

---

## 15. Implementation Status
**Documented**  
*(Documented at Proposal specification level; no business notification dispatch logic or database tables exist in the current skeleton.)*
