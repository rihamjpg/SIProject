import api from "./api";
import { PaginatedAttendance } from "@/types/attendance";

export const attendanceService = {
  getAll: async (page: number = 1): Promise<PaginatedAttendance> => {
    const { data } = await api.get(`/pointages/?page=${page}`);
    return data;
  },
};
