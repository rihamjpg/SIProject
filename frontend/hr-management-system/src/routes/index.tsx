import { Routes, Route } from "react-router-dom";
import { MainLayout } from "@/components/layout/MainLayout";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { LoginForm } from "@/components/auth/LoginForm";
import DashboardPage from "@/pages/dashboard/DashboardPage";
import EmployeesPage from "@/pages/employees/EmployeesPage";
import { LeavesPage } from "@/pages/leaves/LeavesPages";
import AnalyticsPage from "@/pages/analytics/AnalyticsPage";
import { EmployeeDetails } from "@/pages/employees/EmployeeDetails";
import { AddEmployeePage } from "@/pages/employees/AddEmployeePage";
import { ContractsPage } from "@/pages/contracts/ContractsPage";
import { SalariesPage } from "@/pages/salaries/SalariesPage";
import { AttendancePage } from "@/pages/attendance/AttendancePage";
import { HistoryPage } from "@/pages/history/HistoryPage";
import { EvaluationsPage } from "@/pages/evaluation/EvaluationPage";
import { ApplicationsPage } from "@/pages/application/ApplicationsPage";
import { SkillsPage } from "@/pages/skill/SkillsPage";
import { MassroufPage } from "@/pages/massrouf/MassroufPage";
import { RecruitmentsPage } from "@/pages/recruitement/RecruitementsPage";
import { RegisterForm } from "@/components/auth/RegisterForm";

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/register" element={<RegisterForm />} />
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
        <Route path="leaves" element={<LeavesPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="/employees/:id" element={<EmployeeDetails />} />
        <Route path="/employees/add" element={<AddEmployeePage />} />
        <Route path="/contracts" element={<ContractsPage />} />
        <Route path="/salaries" element={<SalariesPage />} />
        <Route path="/attendance" element={<AttendancePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/evaluations" element={<EvaluationsPage />} />
        <Route path="/applications" element={<ApplicationsPage />} />
        <Route path="/skills" element={<SkillsPage />} />
        <Route path="/massrouf" element={<MassroufPage />} />
        <Route path="/recruitments" element={<RecruitmentsPage />} />

        <Route path="*" element={<div>404 Not Found</div>} />
      </Route>
    </Routes>
  );
};
