import api from "./api";
import { PaginatedEvaluations, Evaluation } from "@/types/evaluation";

export const evaluationService = {
  getAll: async (): Promise<PaginatedEvaluations> => {
    const { data } = await api.get("/evaluations/");
    return data;
  },

  getById: async (id: number): Promise<Evaluation> => {
    const { data } = await api.get(`/evaluations/${id}/`);
    return data;
  },
};
