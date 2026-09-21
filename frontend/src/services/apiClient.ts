/**
 * CaseTree AI — Centralized Axios API Client
 *
 * RULE: All API calls go through this client — never call FastAPI directly.
 * RULE: Never store secrets in frontend environment variables.
 */

import axios from "axios";
import type { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "../stores/authStore";

const BASE_URL: string = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080/api";

const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().accessToken;
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = useAuthStore.getState().refreshToken;
      if (refreshToken) {
        try {
          const response = await axios.post(`${BASE_URL}/auth/refresh`, { refreshToken });
          const { accessToken } = response.data.data;
          useAuthStore.getState().setTokens(accessToken, refreshToken);
          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
          return apiClient(originalRequest);
        } catch {
          useAuthStore.getState().logout();
        }
      } else {
        useAuthStore.getState().logout();
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
