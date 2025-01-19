import { Navigate, useLocation } from "react-router-dom";
import { authService } from "@/services/auth";

export const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();

  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
