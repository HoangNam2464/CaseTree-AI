/**
 * EduBranch AI — Shared TypeScript Types
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
// Decision Tree Case
// ============================================================================
export type CaseStatus = "DRAFT" | "REVIEWED" | "APPROVED" | "PUBLISHED";

export interface Case {
  id: string;
  title: string;
  description?: string;
  courseId: string;
  status: CaseStatus;
  version: number;
  rootNodeId?: string;
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
// Simulation Session
// ============================================================================
export interface SimulationSession {
  id: string;
  studentId: string;
  caseId: string;
  currentNodeId?: string;
  completed: boolean;
  startedAt: string;
  completedAt?: string;
}

// ============================================================================
// Student Argument
// ============================================================================
export interface StudentArgument {
  id: string;
  sessionId: string;
  caseId: string;
  nodeId: string;
  optionId: string;
  argumentText: string;
  submittedAt: string;
}

// ============================================================================
// Debate
// ============================================================================
export type MessageRole = "AI_ASSISTANT" | "STUDENT";

export interface DebateMessage {
  id: string;
  sessionId: string;
  roundNumber: number;
  role: MessageRole;
  content: string;
  createdAt: string;
}

export interface DebateSession {
  id: string;
  argumentId: string;
  currentRound: number;
  completed: boolean;
  messages: DebateMessage[];
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
