# EduBranch AI — Evaluation & Research Design

**Status**: Scaffolded (architectural boundary only)

---

## Purpose

This boundary supports the quantitative research dimension of EduBranch AI,
enabling comparison between AI-generated cases and lecturer-authored cases,
and tracking student engagement with the debate mechanism.

---

## Planned Components (not yet implemented)

### Rubric System
- Lecturers define rubrics for evaluating student arguments
- Rubrics linked to courses or specific cases

### Evaluation Records
- Lecturers manually link rubric criteria to simulation sessions
- Store evaluation results per session/argument

### Survey / Data Collection
- Post-simulation survey capture
- Student self-assessment

### Research Dataset Export
- Anonymized export of:
  - Branch selection patterns
  - Argument quality (rubric scores)
  - Debate engagement metrics
  - AI-generated vs lecturer-authored case comparison

---

## Privacy Requirements

- All research dataset exports MUST be anonymized (no PII)
- Student data may only be used for the research purpose with consent
- Personal identifiers must be removed before export

---

## Implementation Status

| Component | Status |
|---|---|
| Evaluation entity | Scaffolded |
| Rubric entity | Scaffolded |
| Survey capture | Planned |
| Dataset export | Planned |
| AI vs Human case comparison | Planned |

> This module will be implemented in a later phase, after the core MVP is complete.
