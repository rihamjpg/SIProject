import api from "./api";
import { PaginatedSalaries } from "@/types/salary";

export const salaryService = {
  getAll: async (page: number = 1): Promise<PaginatedSalaries> => {
    const { data } = await api.get(`/salaries/?page=${page}`);
    return data;
  },
  generatePaySlip: async (id: number) => {
    const { data } = await api.post(`/salaries/${id}/generate-slip/`);
    return data;
  },
};
