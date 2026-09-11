import { Navigate } from "react-router-dom";
import { useAuthStore } from "../../stores/authStore";
import type { Role } from "../../types";
import type { ReactNode } from "react";

interface PrivateRouteProps {
  children: ReactNode;
  role?: Role;
}

export function PrivateRoute({ children, role }: PrivateRouteProps) {
  const { isAuthenticated, user } = useAuthStore();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (role && user?.role !== role) {
    const home = user?.role === "LECTURER" ? "/lecturer/courses" : "/student";
    return <Navigate to={home} replace />;
  }
  return <>{children}</>;
}
