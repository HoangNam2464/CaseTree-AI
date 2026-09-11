/**
 * EduBranch AI — Authentication State Store (Zustand)
 */

import { create } from "zustand";
import type { User } from "../types";

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  setUser: (user: User) => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
  isLecturer: () => boolean;
  isStudent: () => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: true }),
  setTokens: (accessToken, refreshToken) => set({ accessToken, refreshToken }),
  logout: () => set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false }),
  isLecturer: () => get().user?.role === "LECTURER",
  isStudent: () => get().user?.role === "STUDENT",
}));
