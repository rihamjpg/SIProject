import api from "./api";
import {
  RecruitmentStats,
  LeaveStats,
  EvaluationStats,
  AttendanceStats,
} from "@/types/statistics";

export const dashboardService = {
  getRecruitmentStats: async (): Promise<RecruitmentStats> => {
    const { data } = await api.get("/recruitments/statistics");
    return data;
  },
  getLeaveStats: async (): Promise<LeaveStats> => {
    const { data } = await api.get("/leaves/statistics");
    return data;
  },
  getEvaluationStats: async (): Promise<EvaluationStats> => {
    const { data } = await api.get("/evaluations/statistics");
    return data;
  },
  getAttendanceStats: async (): Promise<AttendanceStats> => {
    const { data } = await api.get("/pointages/statistics");
    return data;
  },
};
