import { Routes, Route } from "react-router-dom";
import { MainLayout } from "@/components/layout/MainLayout";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { LoginForm } from "@/components/auth/LoginForm";
import DashboardPage from "@/pages/dashboard/DashboardPage";
import EmployeesPage from "@/pages/employees/EmployeesPage";
// import LeavesPage from "@/pages/leaves/LeavesPage";
import AnalyticsPage from "@/pages/analytics/AnalyticsPage";
import { EmployeeDetails } from "@/pages/employees/EmployeeDetails";
import { AddEmployeePage } from "@/pages/employees/AddEmployeePage";

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="employees" element={<EmployeesPage />} />
        {/* <Route path="leaves" element={<LeavesPage />} /> */}
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="/employees/:id" element={<EmployeeDetails />} />
        <Route path="/employees/add" element={<AddEmployeePage />} />
      </Route>
    </Routes>
  );
};
