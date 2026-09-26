# Feature: Quantitative Evaluation & Research Methodology

> **Authoritative Traceability**: Items 28, 29, 30 (Proposal Section 2 p. 6, Section 4 p. 7, Section 6 p. 10, Section 10 p. 14)  
> **Target Package / Module**: Backend `evaluation/` · AI Service `evaluation/` · Research Boundary  
> **Implementation Method Status**: **`Open / To Be Decided`** (both manual in-platform rubric scoring and structured offline data export are documented as future implementation options pending Project Owner confirmation).

---

## 1. Purpose
Supports the core empirical research contribution of the Capstone project. Provides an evaluation methodology to answer the confirmed **Research Question** from the Proposal:
> *"Evaluate the quality of AI-generated cases (produced from a lecturer's teaching material via RAG) compared with lecturer-authored cases, based on a rubric covering realism, difficulty, and alignment with the course content."*

---

## 2. Actors
- **Lecturer / Evaluator**: Assesses case studies against educational rubrics.
- **Student**: Participates in the classroom trial and completes post-outcome/post-case evaluation surveys.
- **Research Lead (Product / QA)**: Analyzes quantitative outcomes, calculates statistical metrics, and prepares research findings.

---

## 3. Scope
- Defining rubric criteria for evaluating case studies:
  1. **Realism**: Plausibility of situations, options, and consequences.
  2. **Difficulty**: Cognitive challenge, trade-off complexity, ambiguity.
  3. **Course Alignment**: Grounding in authentic syllabus and lecture materials.
- Tracking student reasoning metrics and challenge support engagement depth.
- Future evaluation options:
  - **Option 1**: In-Platform Manual Rubric Scoring (lecturer scores cases and arguments directly in the UI).
  - **Option 2**: Structured Data Export (CSV/JSON) for offline statistical analysis.
- Privacy-preserving, anonymized research dataset generation for capstone deliverables.

---

## 4. Functional Requirements
- **FR-EVAL-01**: The system shall support rubric-based evaluation criteria covering:
  - Realism (1–5 Likert scale)
  - Difficulty (1–5 Likert scale)
  - Alignment with course content (1–5 Likert scale)
- **FR-EVAL-02**: The system shall allow comparative evaluation between AI-generated cases (via RAG) and traditional lecturer-authored cases.
- **FR-EVAL-03**: The system shall capture student self-reported engagement and critical thinking survey responses post-activity.
- **FR-EVAL-04**: The system shall support structured data export of anonymized activity results:
  - Branch selection distributions
  - Word counts and reasoning lengths
  - Number of challenge support rounds engaged (0, 1, or 2)
  - Rubric ratings assigned by evaluators
- **FR-EVAL-05**: All exported research datasets MUST strip Personally Identifiable Information (PII) including student names, emails, and student IDs.

---

## 5. Main Flow (Research Experiment Workflow)
1. **Case Setup**: The lecturer selects a course topic; one case is authored manually, while a paired case is generated via Edu-Branch-AI's RAG pipeline.
2. **Classroom Trial**: Students are divided into cohorts to complete cases, make decisions, submit reasoning/solutions, and interact with AI challenge support.
3. **Rubric Evaluation**: Evaluators assess the cases using the standardized rubric (covering Realism, Difficulty, and Alignment).
4. **Survey Capture**: Students complete a short post-case questionnaire regarding cognitive load and reasoning challenge.
5. **Data Export & Analysis**: The research dataset is exported in anonymized format for comparative statistical analysis (e.g. t-tests or Mann-Whitney U tests comparing AI vs. human case ratings).

---

## 6. Inputs
- Rubric Ratings: `caseId` (UUID), `evaluatorId` (UUID), `realismScore` (1–5), `difficultyScore` (1–5), `alignmentScore` (1–5), `qualitativeNotes` (text).
- Post-Case Survey: `attemptId` / `submissionId` (UUID), `surveyResponses` (key-value ratings).

---

## 7. Outputs
- Evaluation Record: `{ evaluationId, caseId, averageRealism, averageDifficulty, averageAlignment }`.
- Anonymized Dataset File: CSV or JSON export containing trial logs, branch choices, challenge support round counts, and rubric scores.

---

## 8. Business Rules
- **BR-EVAL-01**: **Academic Privacy**: Research dataset exports MUST be strictly anonymized before being shared or published.
- **BR-EVAL-02**: **No AI Self-Grading**: Case evaluation and rubric scoring are conducted by human lecturers or expert evaluators, NOT by autonomous LLMs.
- **BR-EVAL-03**: **Implementation Flexibility**: Whether scoring is handled via in-platform forms or structured export for external tools (e.g. SPSS, R, Excel) is marked `Open / To Be Decided` and does not block MVP skeleton stability.

---

## 9. Permissions
- Role `LECTURER`: Access to evaluation rubrics and course-level export tools.
- Role `STUDENT`: Read-only access to post-case survey forms.
- Public: Never exposed publicly.

---

## 10. Dependencies
- Course and Case domain entities.
- Branching attempts, student reasoning, review submissions, and challenge support history logs.

---

## 11. Data Involved
- Future Conceptual Schema:
  - `evaluations`: Links `case_id`, `evaluator_id`, rubric scores, and timestamps.
  - `surveys`: Stores anonymized student feedback linked to `branching_attempts` or `review_study_submissions`.

---

## 12. Error / Edge Cases
- Insufficient trial sample size: System flags warning if cohort completion is below threshold for statistical significance.
- PII leakage risk: Export sanitization filter verifies that no email or student ID columns are included in research files.

---

## 13. Out of Scope
- Automated peer-to-peer student grading of fellow students' arguments.
- Multi-institutional automated research consortium dashboards.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 28, 29, 30)
- [`docs/research/EVALUATION-DESIGN.md`](../research/EVALUATION-DESIGN.md)

---

## 15. Implementation Status
**Documented**  
*(Detailed evaluation specification established; entities and export services remain unimplemented pending Project Owner confirmation of the evaluation method.)*
