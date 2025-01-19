import api from "./api";
import { PaginatedRecruitments } from "@/types/recruitment";

export const recruitmentService = {
  getAll: async (): Promise<PaginatedRecruitments> => {
    const { data } = await api.get("/recruitments/");
    return data;
  },
};
