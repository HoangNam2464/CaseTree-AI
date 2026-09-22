/**
 * CaseTree AI — Shared TypeScript Types
 *
 * All types mirror the Backend Gateway API response structures.
 */

// ============================================================================
// Auth & User
// ============================================================================
export type Role = "LECTURER" | "STUDENT";

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: Role;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  fullName: string;
  role: Role;
}

// ============================================================================
// Course
// ============================================================================
export interface Course {
  id: string;
  name: string;
  description?: string;
  courseCode?: string;
  lecturerId: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
}

// ============================================================================
// Teaching Material
// ============================================================================
export type ProcessingStatus = "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";

export interface TeachingMaterial {
  id: string;
  originalFilename: string;
  mimeType: string;
  sizeBytes: number;
  courseId: string;
  processingStatus: ProcessingStatus;
  chunkCount?: number;
  uploadedAt: string;
}

// ============================================================================
// Learning Mode
// ============================================================================
export type LearningMode = "BRANCHING_STUDY" | "REVIEW_STUDY";

// ============================================================================
// Case
// ============================================================================
export type CaseStatus = "DRAFT" | "REVIEWED" | "APPROVED" | "PUBLISHED";

export interface Case {
  id: string;
  title: string;
  description?: string;
  courseId: string;
  learningMode: LearningMode;
  contextText?: string;    // REVIEW_STUDY only
  problemText?: string;    // REVIEW_STUDY only
  status: CaseStatus;
  version: number;
  rootNodeId?: string;     // BRANCHING_STUDY only
  createdAt: string;
  updatedAt: string;
}

export interface CaseNode {
  id: string;
  caseId: string;
  situation: string;
  isTerminal: boolean;
  nodeIndex?: number;
  options: CaseOption[];
}

export interface CaseOption {
  id: string;
  nodeId: string;
  text: string;
  consequence: string;
  nextNodeId?: string;
}

// ============================================================================
// Reflection (shared concept, two modes)
// ============================================================================
export type ReflectionStatus = "NOT_STARTED" | "SUBMITTED";

// ============================================================================
// Branching Study
// ============================================================================
export interface BranchingAttempt {
  id: string;
  studentId: string;
  caseId: string;
  attemptNumber: number;
  currentNodeId?: string;
  outcomeNodeId?: string;
  completed: boolean;
  reflectionText?: string;
  reflectionStatus: ReflectionStatus;
  reflectionSubmittedAt?: string;
  startedAt: string;
  completedAt?: string;
}

export interface StudentReasoning {
  id: string;
  attemptId: string;
  nodeId: string;
  selectedOptionId: string;  // always set in Branching Study
  reasoningText: string;
  submittedAt: string;
}

// ============================================================================
// Review Study
// ============================================================================
export type SubmissionStatus = "SUBMITTED" | "REVIEWED" | "REFLECTED";

export interface ReviewStudySubmission {
  id: string;
  studentId: string;
  caseId: string;
  studentAnalysis?: string;  // R2 = CONFIRMED OPTION A: nullable
  proposedSolution: string;
  reasoningText: string;
  submissionStatus: SubmissionStatus;
  reflectionText?: string;
  reflectionStatus: ReflectionStatus;
  reflectionSubmittedAt?: string;
  submittedAt: string;
}

// ============================================================================
// AI Reasoning / Challenge Support (both modes)
// ============================================================================
export type ChallengeMessageRole = "CHALLENGE_SUPPORT" | "STUDENT";

export interface ChallengeMessage {
  id: string;
  sessionId: string;
  roundNumber: number;     // 1 or 2
  role: ChallengeMessageRole;
  content: string;
  createdAt: string;
}

export interface ChallengeSupportSession {
  id: string;
  reasoningId?: string;        // set when Branching Study
  reviewSubmissionId?: string; // set when Review Study
  currentRound: number;        // 0-2
  completed: boolean;
  messages: ChallengeMessage[];
}

// ============================================================================
// Lecturer Feedback (both modes)
// ============================================================================
export interface LecturerFeedback {
  id: string;
  lecturerId: string;
  branchingAttemptId?: string;  // set when Branching Study
  reviewSubmissionId?: string;  // set when Review Study
  feedbackText: string;
  createdAt: string;
}

// ============================================================================
// API Response Wrapper
// ============================================================================
export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data: T;
}

export interface PagedResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  page: number;
  size: number;
}
